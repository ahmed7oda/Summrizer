import re
import fitz  # PyMuPDF
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from pathlib import Path

# nltk for tokenization (optional)
from nltk.tokenize import sent_tokenize

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        text = ''
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        return text

def clean_text(text):
    # Custom text cleaning for accounting content
    # Remove page numbers, headers, footers, etc.
    cleaned_text = text

    # Remove page numbers
    cleaned_text = re.sub(r'\b\d+\b', '', cleaned_text)

    # Add more custom cleaning steps as needed

    return cleaned_text

def recognize_mathematical_formulas(page):
    # You may need to enhance this function based on the specifics of your documents
    # For simplicity, this example looks for text blocks containing mathematical symbols
    formulas = []
    for block in page.get_text("blocks"):
        if any(char.isdigit() or char in "+-*/=(){}[]^_ " for char in block[4]):
            formulas.append(block[4])
    return formulas

def summarize_accounting_pdf(pdf_path, sentences_count=5, exclude_pages=None):
    # Use Sumy for summarization
    summarizer = LexRankSummarizer()

    # Extract the filename and remove the extension
    pdf_filename = Path(pdf_path).stem

    # Create the doc file path (Path from pathlib library)
    doc_path = Path(pdf_path).parent / f"{pdf_filename}_summary.doc"
    
    # Write the summary to the doc file
    with doc_path.open("w", encoding="utf-8") as f:
        f.write(f"Financial Summary of {pdf_filename}:\n\n")

        # Extract text from PDF using PyMuPDF
        with fitz.open(pdf_path) as pdf_document:
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]

                # Skip excluded pages
                if exclude_pages and page_num + 1 in exclude_pages:
                    continue

                # Recognize and include mathematical formulas
                formulas = recognize_mathematical_formulas(page)

                # Customized processing for accounting books
                cleaned_text = clean_text(page.get_text())

                # Use Sumy for summarization
                parser = PlaintextParser.from_string(cleaned_text, Tokenizer("english"))
                summary = summarizer(parser.document, sentences_count=sentences_count)

                # Write the summary to the doc file
                f.write(f"\n--- Page {page_num + 1} ---\n")
                f.write(" ".join(formulas) + "\n")  # Include recognized formulas

                # Convert each sentence to a string before joining
                f.write(" ".join(str(sentence) for sentence in summary) + "\n")

    print("\n--- Financial Summary ---")
    print(f"Source PDF: {pdf_path}\n")
    print(f"Summary saved to: {doc_path}\n")

# Example usage
pdf_path = "c:/Users/Ahmed/Desktop/S/15626.pdf"
summarize_accounting_pdf(pdf_path, sentences_count=100, exclude_pages=[1, 2,5,6])  # Adjust the sentences_count and exclude_pages parameters as needed
