import PyPDF2
from PyPDF2.generic import RectangleObject


def main():
    pdfs = [PyPDF2.PdfFileReader(f'{x + 1}.pdf') for x in range(5)]
    output = PyPDF2.PdfFileMerger()
    for x in pdfs:
        output.append(x)

    with open("merged.pdf", "wb") as o:
        output.write(o)

    merged_pdf = PyPDF2.PdfFileReader("merged.pdf")
    # numbered_pdf = PdfFileWriter()
    total_pages = merged_pdf.getNumPages()
    for p in range(total_pages):
        page: PyPDF2.pdf.PageObject = merged_pdf.getPage(p)
        crop_box: RectangleObject = page.cropBox
        lower_left = crop_box.lowerLeft
        lower_right = crop_box.lowerRight
        upper_left = crop_box.upperLeft
        upper_right = crop_box.upperRight
        print(lower_left)
        print(lower_right)
        print(upper_left)
        print(upper_right)

    # with open("numbered.pdf", "wb") as p:
    #     numbered_pdf.write(o)


if __name__ == "__main__":
    main()
