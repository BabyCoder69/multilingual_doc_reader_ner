import pdfplumber


# Extract text from a PDF
def extract_tables_from_pdf(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # text = page.extract_tables()
            # print(text)
            # formatted_text = page.extract_text(layout=True)  # Preserves layout
            formatted_text = page.extract_text()  # Preserves layout
            print(formatted_text)

            print("#"*30)

            tables = page.extract_tables()
            for table in tables:
                print("Table:", table)
                print("--"*30)

            return {
                "tables": tables,
                "formatted_text": formatted_text
            }


