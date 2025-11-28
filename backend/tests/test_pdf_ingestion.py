from backend.datastore.pdf_reader import PDFReader


def test_pdf_reader_basic():
    reader = PDFReader()
    # Since extract_text will handle input gracefully, test a fake path
    text = reader.extract_text("non_existing.pdf")
    assert isinstance(text, str)
