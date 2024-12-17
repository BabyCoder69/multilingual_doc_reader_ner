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

    def process_booking_details(self, text, entire_text):
        questions = list(self.extraction_model["booking_details"].keys())
        return self.ner_inst.process_section_l1(questions=questions, section_text=text, entire_text=entire_text)

    def process_shipment_route(self, text, entire_text):
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

    def process_cargo_information(self, text, entire_text):
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

    def process_vessel_information(self, text, entire_text):
        return self.ner_inst.process_section_l1(questions=list(self.extraction_model["vessel_information"].keys()),
                                                section_text=text,
                                                entire_text=entire_text)

    def process_parties_information(self, text, entire_text):
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
