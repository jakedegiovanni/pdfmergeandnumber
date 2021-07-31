import os
import typing

import PyPDF2
from fpdf import FPDF

MERGED_PDF_FILENAME = "merged.pdf"
TEMP_NUMBERED_PDF_FILENAME = "temp_numbered.pdf"
NUMBERED_PDF_FILENAME = "numbered.pdf"


# https://pyfpdf.github.io/fpdf2/Tutorial.html#tuto-2-header-footer-page-break-and-image
# https://stackoverflow.com/questions/54931322/adding-page-number-while-merge-a-pdf-with-pypdf2
class NumberedPDF(FPDF):
    def __init__(self, total_pages):
        super(NumberedPDF, self).__init__()
        self.total_pages = total_pages

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.cell(0, 10, f'{self.page_no()}', 0, 0, 'C')


def main():
    source_pdfs = get_source_pdfs()

    merge_source_pdfs(source_pdfs)

    merged_pdf = PyPDF2.PdfFileReader(MERGED_PDF_FILENAME)

    numbered_pdf_template(merged_pdf.getNumPages())

    add_page_numbers_to_merged_pdfs(merged_pdf)

    cleanup()


def get_source_pdfs():
    return [PyPDF2.PdfFileReader(f'{x + 1}.pdf') for x in range(5)]


def merge_source_pdfs(pdfs: typing.List):
    output = PyPDF2.PdfFileMerger()
    for x in pdfs:
        output.append(x)

    with open(MERGED_PDF_FILENAME, "wb") as o:
        output.write(o)


def numbered_pdf_template(total_pages):
    temp_numbered_pdf = NumberedPDF(total_pages)
    for page in range(total_pages):
        temp_numbered_pdf.add_page()
    temp_numbered_pdf.output(TEMP_NUMBERED_PDF_FILENAME)


def add_page_numbers_to_merged_pdfs(merged_pdf):
    numbered_pdf = PyPDF2.PdfFileReader(TEMP_NUMBERED_PDF_FILENAME)
    final_pdf = PyPDF2.PdfFileWriter()

    for x, page in enumerate(numbered_pdf.pages):
        p: PyPDF2.pdf.PageObject = merged_pdf.getPage(x)
        p.mergePage(page)
        final_pdf.addPage(p)

    with open(NUMBERED_PDF_FILENAME, "wb") as o:
        final_pdf.write(o)


def cleanup():
    os.remove(MERGED_PDF_FILENAME)
    os.remove(TEMP_NUMBERED_PDF_FILENAME)


if __name__ == "__main__":
    main()
