import os
import logging
import warnings

from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams
)

from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import (
    HuggingFaceEndpointEmbeddings
)


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("keras").setLevel(logging.ERROR)

warnings.filterwarnings(
    "ignore",
    category=FutureWarning
)

warnings.filterwarnings(
    "ignore",
    module="tensorflow"
)

load_dotenv()


COLLECTION_NAME = "enterprise_docs"

QDRANT_URL = "http://localhost:6333"


embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=
    os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
)


client = QdrantClient(
    url=QDRANT_URL
)



def create_collection_if_not_exists():

    collections = client.get_collections()

    collection_names = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in collection_names:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,             
                distance=Distance.COSINE
            )
        )

        print(
            f"Created collection: "
            f"{COLLECTION_NAME}"
        )

    else:

        print(
            f"Collection already exists: "
            f"{COLLECTION_NAME}"
        )

create_collection_if_not_exists()


def get_vector_store():

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )

def ingest_documents(chunks):

    if not chunks:

        print("No chunks found.")

        return

    vector_store = get_vector_store()

    vector_store.add_documents(
        documents=chunks
    )

    print(
        f"{len(chunks)} chunks "
        f"inserted into Qdrant."
    )