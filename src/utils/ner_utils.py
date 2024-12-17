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
        """
        Predicts Named Entity Recognition (NER) labels for the given text.

        This function uses a pre-trained NER model to predict entity labels based on the provided
        text and a list of target labels.

        Args:
            text (str): The input text for which NER labels need to be predicted.
            labels (list): A list of entity labels to predict.

        Returns:
            dict: A dictionary containing the predicted entities, where the keys are the entity labels
                  and the values are the corresponding extracted text or entities.
        """

        try:
            logger.info("Predicting NER labels...")
            return self.model.predict_entities(text, labels)
        except Exception as e:
            logger.error(f"Error while predicting NER labels: {e}")

    def process_section_l1(self, questions, section_text, entire_text):
        """
        Processes a section of text to extract answers for specified questions using NER and LLM models.

        This function processes a given section of text and uses a combination of Named Entity Recognition (NER)
        and a language model (LLM) to extract answers for a list of questions. If the NER prediction confidence
        is below a specified threshold, the LLM is used as a fallback to provide an answer.

        Args:
            questions (list): A list of questions for which answers need to be extracted.
            section_text (str): The specific section text to be processed.
            entire_text (str): The full text that can be used as context for fallback answers.

        Returns:
            dict: A dictionary where the keys are the questions and the values are dictionaries containing:
                  - "value" (str): The extracted answer text.
                  - "confidence" (float): The confidence score of the prediction.

        """

        try:

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
        except Exception as e:
            logger.error(f"Error while processing section: {e}")

    def process_section_l2(self, questions, sub_section, section, section_text, entire_text):
        """
        Processes a subsection of text to extract answers for specified questions using NER and LLM models.

        This function processes a given subsection within a section of text and uses a combination of Named Entity Recognition (NER)
        and a language model (LLM) to extract answers for a list of questions. If the NER prediction confidence
        is below a specified threshold, the LLM is used as a fallback to provide an answer.

        Args:
            questions (list): A list of questions for which answers need to be extracted.
            sub_section (str): The name of the specific subsection being processed.
            section (str): The parent section that contains the subsection.
            section_text (str): The specific subsection text to be processed.
            entire_text (str): The full text that can be used as context for fallback answers.

        Returns:
            dict: A dictionary where the keys are the questions and the values are dictionaries containing:
                  - "value" (str): The extracted answer text.
                  - "confidence" (float): The confidence score of the prediction.
        """

        try:
            processed_text = self.process_text(section_text)
            entire_text = self.process_text(entire_text)

            section_res = {}

            for question in questions:
                _q = f"What is the {question} of the {sub_section} of the {section}?\n"
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
        except Exception as e:
            logger.error(f"Error while processing section: {e}")