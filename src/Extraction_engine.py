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

    @staticmethod
    def init_extraction_model():
        return {
            'booking_details': ['booking_number', 'service_contract_number'],
            'shipment_route': ['origin', 'destination', 'transit_ports'],
            'cargo_information': ['cargo_type', 'cargo_description', 'container_details', 'total_weight'],
            'vessel_information': ['vessel_name', 'vessel_voyage', 'estimated_departure', 'estimated_arrival'],
            'parties_information': ['shipper', 'carrier']
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


    def process_pdf(self, pdf_path):
        pages = extract_text_from_pdf(pdf_path)

        translated_pages = [self.llm_inst.determine_language_and_translate(text=page) for page in pages]

        agg_sections = self.aggregate_sections(pages=translated_pages)

        final_doc = {}

        entire_text = "\n".join(value for value in agg_sections.values())

        for sec, sec_text in agg_sections.items():
            final_doc[sec] = self.ner_inst.process_section(questions=self.extraction_model[sec],
                                                           section_text=sec_text,
                                                           entire_text=entire_text)

        return final_doc

