import merge


def main():
    source_pdfs = get_source_pdfs()
    merge.merge_and_number(source_pdfs)


def get_source_pdfs():
    return [f'{x + 1}.pdf' for x in range(5)]


if __name__ == "__main__":
    main()
