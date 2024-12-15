import json
import openai
from groq import Groq
import re
from typing import List


from src.config import ConfigUtility

opai_client = openai.OpenAI(
    api_key=ConfigUtility.OPENAI_API_KEY,  # Please Replace with your OpenAI API key to run the code
)

groq_client = Groq(
    api_key=ConfigUtility.GROQ_API_KEY,
)


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



def is_non_english(text: str) -> bool:
    """
    Check if a line contains any non-English characters.
    """
    return bool(re.search(r'[^\x00-\x7F]', text))  # Matches non-ASCII characters


def translate_text(text: List[str]) -> List[str]:
    """
    Translate non-English text lines.
    Placeholder function for actual translation logic.
    Replace with API call or translation method.
    """
    translated_lines = []
    for line in text:
        # Mock translation: Prepend "Translated:" to simulate translation
        translated_lines.append(f"Translated: {line}")
    return translated_lines


def process_text(text) -> List[str]:
    """
    Process the text by identifying non-English lines, translating them,
    and merging all lines back in the original order.
    """

    lines = text.split('\n')

    non_english_lines = []
    untranslated_lines = []
    translation_indices = []

    # Separate lines needing translation
    for idx, line in enumerate(lines):
        if is_non_english(line):
            non_english_lines.append(line)
            translation_indices.append(idx)  # Track the index for merging later
        else:
            untranslated_lines.append((idx, line))

    # Translate non-English lines
    translated_lines = translate_text(non_english_lines)

    # Merge translated and untranslated lines
    all_lines = untranslated_lines + list(zip(translation_indices, translated_lines))
    all_lines.sort(key=lambda x: x[0])  # Sort by original indices

    # Extract the merged text in the correct order
    final_text = [line for _, line in all_lines]
    return final_text



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


def determine_language_and_translate(text):
    res = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": """You are a translator. Translate the given text to into English.

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