from src.utils.pdf_utils import extract_tables_from_pdf
from src.utils.ner_utils import determine_language_and_translate, process_text



a = extract_tables_from_pdf("Posco_Logistics.pdf")

b = determine_language_and_translate(text=a["formatted_text"])
# b = process_text(text=a["formatted_text"])

print(b)