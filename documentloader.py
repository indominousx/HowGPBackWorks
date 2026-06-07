import os
import logging
import warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("keras").setLevel(logging.ERROR)

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", module="tensorflow")
warnings.filterwarnings(
    "ignore",
    message=".*sparse_softmax_cross_entropy.*"
)

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_pdf_chunks(file_paths, chat_id):
    """
    Loads multiple PDFs, splits them into chunks,
    and attaches metadata for Qdrant filtering.
    """

    all_chunks = []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    for file_path in file_paths:

        try:
            loader = PyMuPDFLoader(file_path)

            documents = loader.load()

            chunks = text_splitter.split_documents(documents)

            file_name = os.path.basename(file_path)

            for chunk in chunks:

                chunk.metadata.update(
                    {
                        "chat_id": chat_id,
                        "file_name": file_name
                    }
                )

            all_chunks.extend(chunks)

            print(
                f"Loaded {file_name} | "
                f"{len(chunks)} chunks generated"
            )

        except Exception as e:

            print(
                f"Error processing {file_path}: {e}"
            )

    print(
        f"Total chunks created: {len(all_chunks)}"
    )
    print(chunks[0].metadata)
    return all_chunks