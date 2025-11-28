from backend.datastore.text_splitter import TextSplitter

def test_text_splitter():
    splitter = TextSplitter(chunk_size=50)
    chunks = splitter.split_text("This is a test sentence that should be chunked.")
    assert isinstance(chunks, list)
    assert len(chunks) >= 1
