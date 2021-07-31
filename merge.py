import os
import typing

import PyPDF2
from fpdf import FPDF

MERGED_PDF_FILENAME = "merged.pdf"
TEMP_NUMBERED_PDF_FILENAME = "temp_numbered.pdf"


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


def merge_and_number(source_pdfs: typing.List[str], output_file: typing.Optional[typing.TextIO]):
    # todo: try catch finally
    merged_pdf = _merge(source_pdfs)
    numbered_pdf_template = _generate_numbered_pdf_template(merged_pdf.getNumPages())
    _add_page_numbers_to_merged_pdfs(numbered_pdf_template, merged_pdf, output_file)
    _cleanup()


def _merge(source_pdfs: typing.List[str]) -> PyPDF2.PdfFileReader:
    merged_pdf = PyPDF2.PdfFileMerger()
    for x in source_pdfs:
        p = PyPDF2.PdfFileReader(x)
        merged_pdf.append(p)

    with open(MERGED_PDF_FILENAME, "wb") as o:
        merged_pdf.write(o)

    return PyPDF2.PdfFileReader(MERGED_PDF_FILENAME)


def _generate_numbered_pdf_template(total_pages: int) -> PyPDF2.PdfFileReader:
    temp_numbered_pdf = NumberedPDF(total_pages)
    for page in range(total_pages):
        temp_numbered_pdf.add_page()
    temp_numbered_pdf.output(TEMP_NUMBERED_PDF_FILENAME)

    return PyPDF2.PdfFileReader(TEMP_NUMBERED_PDF_FILENAME)


def _add_page_numbers_to_merged_pdfs(numbered_pdf_template: PyPDF2.PdfFileReader, merged_pdf: PyPDF2.PdfFileReader,
                                     output_file: typing.Optional[typing.TextIO]):
    final_pdf = PyPDF2.PdfFileWriter()

    for x, page in enumerate(numbered_pdf_template.pages):
        p: PyPDF2.pdf.PageObject = merged_pdf.getPage(x)
        p.mergePage(page)
        final_pdf.addPage(p)

    final_pdf.write(output_file)


def _cleanup():
    # todo: check if file exists
    os.remove(MERGED_PDF_FILENAME)
    os.remove(TEMP_NUMBERED_PDF_FILENAME)
