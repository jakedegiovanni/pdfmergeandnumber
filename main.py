import os
import PyPDF2
from fpdf import FPDF


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
    pdfs = [PyPDF2.PdfFileReader(f'{x + 1}.pdf') for x in range(5)]
    output = PyPDF2.PdfFileMerger()
    for x in pdfs:
        output.append(x)

    with open("merged.pdf", "wb") as o:
        output.write(o)

    merged_pdf = PyPDF2.PdfFileReader("merged.pdf")
    numbered_pdf = NumberedPDF(merged_pdf.getNumPages())
    for page in range(merged_pdf.getNumPages()):
        numbered_pdf.add_page()

    numbered_pdf.output("temp_numbered.pdf")

    numbered_pdf = PyPDF2.PdfFileReader("temp_numbered.pdf")
    final_pdf = PyPDF2.PdfFileWriter()
    for x, page in enumerate(numbered_pdf.pages):
        p: PyPDF2.pdf.PageObject = merged_pdf.getPage(x)
        p.mergePage(page)
        final_pdf.addPage(p)

    os.remove("merged.pdf")
    os.remove("temp_numbered.pdf")

    with open("numbered.pdf", "wb") as o:
        final_pdf.write(o)


if __name__ == "__main__":
    main()
