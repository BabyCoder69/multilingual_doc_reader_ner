import json
import logging
from groq import Groq
import time
from functools import wraps

# import openai
# import re
# from typing import List


from src.config import ConfigUtility

# opai_client = openai.OpenAI(
#     api_key=ConfigUtility.OPENAI_API_KEY,  # Please Replace with your OpenAI API key to run the code
# )

# def determine_language_and_translate(text):
#     res = opai_client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": """You are a translator. If the given text is not in English, translate it into English.
#                 """,
#             },
#             {
#                 "role": "user",
#                 "content": f"""
#                 Output the translated text in the following format:
#
#                 class LangTransRes(BaseModel):
#                     required: bool # True if the text is not in English
#                     lang: Optional[str] = None # The language of the text
#                     text: Optional[str] = None # The translated text
#
#                 The text to be translated: {text}
#                 """,
#             },
#         ],
#         n=1,
#         temperature=0.2,
#         response_format={"type": "json_object"}
#     )
#
#     return json.loads(res.choices[0].message.content)



# def is_non_english(text: str) -> bool:
#     """
#     Check if a line contains any non-English characters.
#     """
#     return bool(re.search(r'[^\x00-\x7F]', text))  # Matches non-ASCII characters
#
#
# def translate_text(text: List[str]) -> List[str]:
#     """
#     Translate non-English text lines.
#     Placeholder function for actual translation logic.
#     Replace with API call or translation method.
#     """
#     translated_lines = []
#     for line in text:
#         # Mock translation: Prepend "Translated:" to simulate translation
#         translated_lines.append(f"Translated: {line}")
#     return translated_lines
#
#
# def process_text(text) -> List[str]:
#     """
#     Process the text by identifying non-English lines, translating them,
#     and merging all lines back in the original order.
#     """
#
#     lines = text.split('\n')
#
#     non_english_lines = []
#     untranslated_lines = []
#     translation_indices = []
#
#     # Separate lines needing translation
#     for idx, line in enumerate(lines):
#         if is_non_english(line):
#             non_english_lines.append(line)
#             translation_indices.append(idx)  # Track the index for merging later
#         else:
#             untranslated_lines.append((idx, line))
#
#     # Translate non-English lines
#     translated_lines = translate_text(non_english_lines)
#
#     # Merge translated and untranslated lines
#     all_lines = untranslated_lines + list(zip(translation_indices, translated_lines))
#     all_lines.sort(key=lambda x: x[0])  # Sort by original indices
#
#     # Extract the merged text in the correct order
#     final_text = [line for _, line in all_lines]
#     return final_text



# def determine_language_and_translate(text_list: List[str]):
#     res = groq_client.chat.completions.create(
#         model="llama3-8b-8192",
#         messages=[
#             {
#                 "role": "system",
#                 "content": """You are a translator. You will be given a list of sentences. Translate each sentence to into English.
#
#                 Output the translated text in the following json format:
#
#                 class LangTransRes(BaseModel):
#                     lang: str # The language of the text
#                     text: List[str] # The translated text
#                 """,
#             },
#             {
#                 "role": "user",
#                 "content": f"""
#                 The list of sentences to be translated: {text_list}
#                 """,
#             },
#         ],
#         n=1,
#         temperature=0.2,
#         response_format={"type": "json_object"}
#     )
#
#     return json.loads(res.choices[0].message.content)

logger = logging.getLogger(__name__)


def retry(max_retries=3, delay=2, exceptions=(Exception,)):
    """
    A decorator to retry a function if it raises specific exceptions.

    Args:
        max_retries (int): Maximum number of retry attempts.
        delay (int): Delay in seconds between retries.
        exceptions (tuple): Exceptions to catch and retry.

    Returns:
        function: The wrapped function with retry logic.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    logger.info(f"Retrying {func.__name__} due to {e} ({attempts}/{max_retries})...")
                    time.sleep(delay)
            raise Exception(f"Function {func.__name__} failed after {max_retries} retries.")
        return wrapper
    return decorator



class LLMInference:
    def __init__(self):
        self.groq_client = Groq(
            api_key=ConfigUtility.GROQ_API_KEY,
        )
        self.groq_model = ConfigUtility.GROQ_MODEL

        self._decorate_methods()

    def _decorate_methods(self):
        for attr_name in dir(self):
            if callable(getattr(self, attr_name)) and not attr_name.startswith("_"):
                original_method = getattr(self, attr_name)
                decorated_method = retry(max_retries=3, delay=1)(original_method)
                setattr(self, attr_name, decorated_method)

    def determine_language_and_translate(self, text):
        res = self.groq_client.chat.completions.create(
            model=self.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a translator. Translate the given text to into English.
                    You must remove the terms and conditions section if present before returning the output.
    
                    Output the translated text in the following json format:
    
                    class LangTransRes(BaseModel):
                        lang: str # The language of the text
                        text: str # The translated text
                    """,
                },
                {
                    "role": "user",
                    "content": f"""
                    The text to be translated: {text}
                    """,
                },
            ],
            n=1,
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        return json.loads(res.choices[0].message.content)


    def isolate_sections(self, sections, text):
        res = self.groq_client.chat.completions.create(
            model=self.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a document analyzer. Your job is to split the given text as per the sections given.
                    
                        The sections are: {sections}
    
                        Output the sectioned text in the following json format:
                        """ +
                        """
                        {
                            "section1" : Text belonging to section1,
                            "section2" : Text belonging to section2,
                            ....
                        }
                        """,
                },
                {
                    "role": "user",
                    "content": f"""
                        The text to be sectioned: {text}
                        """,
                },
            ],
            n=1,
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        return json.loads(res.choices[0].message.content)

    def answer_question(self, question, text):
        res = self.groq_client.chat.completions.create(
            model=self.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a document analyzer. Your job is to understand the given question and answer 
                                    it as per the text given in a precise manner without any additional explanations.

                                Output the sectioned text in the following json format:
                                class QA(BaseModel):
                                    text: str # Answer to the question
                                    score: float # range between 0 and 1 indicating the confidence of the answer
                                """,
                },
                {
                    "role": "user",
                    "content": f"""
                                The question: {question},
                                The text: {text}
                                """,
                },
            ],
            n=1,
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        return json.loads(res.choices[0].message.content)