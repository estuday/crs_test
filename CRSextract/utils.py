from langchain_text_splitters import CharacterTextSplitter


def text_split(text: str):

    spliter = CharacterTextSplitter(
        separator="。",
        chunk_size=500,
        chunk_overlap=0,
    )
    return spliter.split_text(text)
