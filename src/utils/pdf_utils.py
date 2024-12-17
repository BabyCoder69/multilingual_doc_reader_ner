import logging
import pdfplumber

logger = logging.getLogger(__name__)


# Extract text from a PDF
def extract_text_from_pdf(pdf_path):
    """
    Extracts text content from a PDF file.

    This function reads a PDF file page by page and extracts the text content from each page.
    The extracted text is returned as a list of strings, where each string represents the text
    content of a single page.

    Args:
        pdf_path (str): The file path to the PDF document.

    Returns:
        list: A list of strings, where each string contains the extracted text from a corresponding page in the PDF.
    """

    try:
        res_pages = []
        logger.info(f"Extracting the text from the PDF: {pdf_path}")
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # text = page.extract_tables()
                # print(text)
                # formatted_text = page.extract_text(layout=True)  # Preserves layout
                formatted_text = page.extract_text()
                res_pages.append(formatted_text)
                # tables = page.extract_tables()
                # for table in tables:
                #     print("Table:", table)
                #     print("--"*30)
                #
                # return {
                #     "tables": tables,
                #     "formatted_text": formatted_text
                # }

        return res_pages
    except Exception as e:
        logger.error(f"Error while extracting text from PDF: {e}")
