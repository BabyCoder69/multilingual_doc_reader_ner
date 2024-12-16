import logging
from gliner import GLiNER

from src.utils.llm_utils import LLMInference

logger = logging.getLogger(__name__)

class NerModel:
    def __init__(self):
        logger.info("Initializing GLiNER model...")
        self.model = GLiNER.from_pretrained("knowledgator/gliner-multitask-v1.0")
        logger.info("GLiNER model initialized.")
        self.llm_inst = LLMInference()

        self.ner_threshold = 0.9

    @staticmethod
    def process_text(text):
        return text.replace("\r\n", "")

    def predict_ner_labels(self, text, labels):
        logger.info("Predicting NER labels...")
        return self.model.predict_entities(text, labels)

    def process_section(self, questions, section_text, entire_text):

        processed_text = self.process_text(section_text)
        entire_text = self.process_text(entire_text)

        section_res = {}

        for question in questions:
            _q = f"What is the {question}?\n"
            _input = _q + processed_text
            ner_res = self.predict_ner_labels(text=_input, labels=["answer"])

            if ner_res:
                ner_pred = max(ner_res, key=lambda x: x['score'])
                if ner_pred["score"] < self.ner_threshold:
                    ner_pred = self.llm_inst.answer_question(question=_q, text=entire_text)
            else:
                ner_pred = self.llm_inst.answer_question(question=_q, text=entire_text)

            section_res[question] = {
                    "value": ner_pred["text"],
                    "confidence": ner_pred["score"]
                }

        return section_res