import json
import logging
from src.utils.pdf_utils import extract_text_from_pdf
from src.utils.ner_utils import NerModel
from src.utils.llm_utils import LLMInference

logger = logging.getLogger(__name__)


class ExtractionEngine:
    def __init__(self):
        self.ner_inst = NerModel()
        self.llm_inst = LLMInference()
        self.extraction_model = self.init_extraction_model()

    # @staticmethod
    # def init_extraction_model():
    #     data = {}
    #     with open("utils\models\model.json", 'r') as file:
    #         json_obj = json.load(file)
    #         for key in json_obj:
    #             data[key] = list(json_obj[key].keys())
    #     return data

    # @staticmethod
    # def init_extraction_model_v1():
    #     return {
    #         'booking_details': ['booking_number', 'service_contract_number'],
    #         'shipment_route': ['origin', 'destination', 'transit_ports'],
    #         'cargo_information': ['cargo_type', 'cargo_description', 'container_details', 'total_weight'],
    #         'vessel_information': ['vessel_name', 'vessel_voyage', 'estimated_departure', 'estimated_arrival'],
    #         'parties_information': ['shipper', 'carrier']
    #     }

    @staticmethod
    def init_extraction_model():
        return {
    "booking_details": {
      "booking_number":  {},
      "service_contract_number": {}
    },
    "shipment_route": {
      "origin": {
        "location": {},
        "terminal": {}
      },
      "destination": {
        "location": {},
        "terminal": {}
      },
      "transit_ports": [
        {
          "port_name": {},
          "eta": {}
        }
      ]
    },
    "cargo_information": {
      "cargo_type":  {},
      "cargo_description": {},
      "container_details": {
        "quantity": {},
        "size": {},
        "type": {}
      },
      "total_weight": {}
    },
    "vessel_information": {
      "vessel_name":  {},
      "vessel_voyage": {},
      "estimated_departure": {},
      "estimated_arrival": {}
    },
    "parties_information": {
      "shipper": {
        "name": {},
        "contact_details": {}
      },
      "carrier": {
        "name": {},
        "contact_details": {}
      }
    }
}


    def aggregate_sections(self, pages):
        """
        Aggregates text content from multiple pages into predefined sections.

        This function processes a list of pages, isolates specific sections from each page using a language model,
        and combines the content of the same sections across pages into a single aggregated result.

        Args:
            pages (list): A list of strings where each string represents the text content of a page.

        Returns:
            dict: A dictionary where the keys are section names (defined in `self.extraction_model`)
                  and the values are the aggregated text content for each section.
        """

        try:
            res = {}
            sections = list(self.extraction_model.keys())
            for page in pages:
                _secs = self.llm_inst.isolate_sections(sections=sections, text=page)

                for _sec in _secs:
                    if _sec in res:
                        res[_sec] += "\n" + _secs[_sec]
                    else:
                        res[_sec] = _secs[_sec]

            return res
        except Exception as e:
            logger.error(f"Error aggregating sections: {e}")

    def process_booking_details(self, text, entire_text):
        """
        Processes booking details from a given text.

        This function extracts booking-related information by applying a named entity recognition (NER)
        model to the provided section text and the entire text. It uses predefined questions
        from the "booking_details" section of the extraction model to guide the extraction process.

        Args:
            text (str): The specific section text containing booking details.
            entire_text (str): The full text from which the section was extracted.

        Returns:
            dict: A dictionary containing the extracted booking details, where the keys are
                  predefined questions and the values are the corresponding extracted information.
        """

        try:
            logger.info("Processing booking details...")
            questions = list(self.extraction_model["booking_details"].keys())
            return self.ner_inst.process_section_l1(questions=questions, section_text=text, entire_text=entire_text)
        except Exception as e:
            logger.error(f"Error processing booking details: {e}")

    def process_shipment_route(self, text, entire_text):
        """
        Processes shipment route information from a given text.

        This function extracts details related to the shipment route, including the origin, destination,
        and transit ports. It uses a named entity recognition (NER) model for structured extraction
        of origin and destination details and a language model (LLM) to identify multiple answers
        for transit ports.

        Args:
            text (str): The specific section text containing shipment route details.
            entire_text (str): The full text from which the section was extracted.

        Returns:
            dict: A dictionary containing the following keys:
                - "origin": Extracted details about the origin section.
                - "destination": Extracted details about the destination section.
                - "transit_ports": A list of answers with port names and estimated times of arrival (ETA).
        """

        try:
            logger.info("Processing shipment route...")
            return {
                "origin": self.ner_inst.process_section_l2(questions=list(self.extraction_model["shipment_route"]["origin"].keys()),
                                                           sub_section="origin",
                                                           section="shipment_route",
                                                           section_text=text,
                                                           entire_text=entire_text),
                "destination": self.ner_inst.process_section_l2(questions=list(self.extraction_model["shipment_route"]["destination"].keys()),
                                                                sub_section="destination",
                                                                section="shipment_route",
                                                                section_text=text,
                                                                entire_text=entire_text),
                "transit_ports": self.llm_inst.find_multiple_answers(question="What are port_name and eta of all the transit_ports?",
                                                                     text=entire_text)
            }
        except Exception as e:
            logger.error(f"Error processing shipment route: {e}")

    def process_cargo_information(self, text, entire_text):
        """
        Processes cargo information from a given text.

        This function extracts cargo-related details such as cargo type, description,
        total weight, and container details. It uses a named entity recognition (NER)
        model for structured extraction of these elements.

        Args:
            text (str): The specific section text containing cargo information.
            entire_text (str): The full text from which the section was extracted.

        Returns:
            dict: A dictionary containing the following keys:
                - "cargo_type": The type of cargo.
                - "cargo_description": A description of the cargo.
                - "container_details": Detailed information about the cargo containers.
                - "total_weight": The total weight of the cargo.
        """

        try:
            logger.info("Processing cargo information...")
            questions = ["cargo_type", "cargo_description", "total_weight"]
            answers = self.ner_inst.process_section_l1(questions=questions, section_text=text, entire_text=entire_text)

            cargo_doc = {
                "cargo_type": answers["cargo_type"],
                "cargo_description": answers["cargo_description"],
                "container_details": self.ner_inst.process_section_l2(questions=list(self.extraction_model["cargo_information"]["container_details"].keys()),
                                                                      sub_section="container_details",
                                                                      section="cargo_information",
                                                                      section_text=text,
                                                                      entire_text=entire_text),
                "total_weight": answers["total_weight"]
            }

            return cargo_doc
        except Exception as e:
            logger.error(f"Error processing cargo information: {e}")

    def process_vessel_information(self, text, entire_text):
        """
        Processes vessel information from a given text.

        This function extracts vessel-related details such as vessel name, voyage,
        and estimated timings. It uses a named entity recognition (NER) model
        to process the section text based on predefined questions.

        Args:
            text (str): The specific section text containing vessel information.
            entire_text (str): The full text from which the section was extracted.

        Returns:
            dict: A dictionary containing the extracted vessel information,
                  where the keys are predefined questions from the "vessel_information" section
                  of the extraction model and the values are the corresponding extracted data.
        """

        try:
            logger.info("Processing vessel information...")
            return self.ner_inst.process_section_l1(questions=list(self.extraction_model["vessel_information"].keys()),
                                                    section_text=text,
                                                    entire_text=entire_text)
        except Exception as e:
            logger.error(f"Error processing vessel information: {e}")

    def process_parties_information(self, text, entire_text):
        """
        Processes parties information from a given text.

        This function extracts details about the shipper and carrier involved in the shipment.
        It uses a named entity recognition (NER) model to process and retrieve structured information
        for each party based on predefined questions.

        Args:
            text (str): The specific section text containing parties information.
            entire_text (str): The full text from which the section was extracted.

        Returns:
            dict: A dictionary containing the following keys:
                - "shipper": Extracted details about the shipper.
                - "carrier": Extracted details about the carrier.
        """

        try:
            logger.info("Processing parties information...")
            return {
                "shipper": self.ner_inst.process_section_l2(questions=list(self.extraction_model["parties_information"]["shipper"].keys()),
                                                            sub_section="shipper",
                                                            section="parties_information",
                                                            section_text=text,
                                                            entire_text=entire_text),
                "carrier": self.ner_inst.process_section_l2(questions=list(self.extraction_model["parties_information"]["carrier"].keys()),
                                                            sub_section="carrier",
                                                            section="parties_information",
                                                            section_text=text,
                                                            entire_text=entire_text)

            }
        except Exception as e:
            logger.error(f"Error processing parties information: {e}")




    # def process_pdf_v1(self, pdf_path):
    #     pages = extract_text_from_pdf(pdf_path)
    #
    #     translated_pages = [self.llm_inst.determine_language_and_translate(text=page) for page in pages]
    #
    #     agg_sections = self.aggregate_sections(pages=translated_pages)
    #
    #     final_doc = {}
    #
    #     entire_text = "\n".join(value for value in agg_sections.values())
    #
    #     for sec, sec_text in agg_sections.items():
    #         final_doc[sec] = self.ner_inst.process_section_l1(questions=self.extraction_model[sec],
    #                                                           section_text=sec_text,
    #                                                           entire_text=entire_text)
    #
    #     return final_doc


    def process_pdf(self, pdf_path):
        """
        Processes a PDF document to extract and structure relevant shipment-related information.

        This function extracts text from a PDF, translates it if necessary, aggregates it into
        predefined sections, and processes each section to retrieve structured details such as
        booking details, shipment route, cargo information, vessel information, and parties involved.

        Args:
            pdf_path (str): The file path to the PDF document.

        Returns:
            dict: A dictionary containing the following keys:
                - "booking_details": Structured information about booking details.
                - "shipment_route": Details of the shipment's route, including origin, destination, and transit ports.
                - "cargo_information": Information about the cargo, including type, description, and weight.
                - "vessel_information": Details of the vessel, such as name, voyage, and timings.
                - "parties_information": Information about the shipper and carrier.

        Steps:
            1. Extracts text from the PDF file.
            2. Translates each page if needed.
            3. Aggregates the text into predefined sections.
            4. Processes each section to extract relevant information.
        """

        try:
            logger.info(f"Processing PDF: {pdf_path}")
            pages = extract_text_from_pdf(pdf_path)

            translated_pages = [self.llm_inst.determine_language_and_translate(text=page) for page in pages]

            agg_sections = self.aggregate_sections(pages=translated_pages)

            entire_text = "\n".join(value for value in agg_sections.values())

            return {
                "booking_details": self.process_booking_details(text=agg_sections["booking_details"],
                                                                entire_text=entire_text),
                "shipment_route": self.process_shipment_route(text=agg_sections["shipment_route"],
                                                              entire_text=entire_text),
                "cargo_information": self.process_cargo_information(text=agg_sections["cargo_information"],
                                                                    entire_text=entire_text),
                "vessel_information": self.process_vessel_information(text=agg_sections["vessel_information"],
                                                                      entire_text=entire_text),
                "parties_information": self.process_parties_information(text=agg_sections["parties_information"],
                                                                        entire_text=entire_text)
            }
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
