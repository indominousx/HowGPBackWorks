import os
import logging
import warnings

from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_huggingface import (
    HuggingFaceEndpoint,
    ChatHuggingFace
)

from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue
)

from genembeddings import client, COLLECTION_NAME
from genembeddings import get_vector_store


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


llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=
    os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN"),

    max_new_tokens=1024,
    temperature=0.1
)

chat_model = ChatHuggingFace(
    llm=llm
)


prompt = PromptTemplate(
    template="""
[ROLE & GOAL]

You are an elite Technical Systems Analyst and
Enterprise Document Intelligence Specialist.

Your sole objective is to answer the User Question
using ONLY the information provided in the Source
Context.

[RULES OF ENGAGEMENT]

1. PRECISE GROUNDING
   Use only information from the Context.

2. NO HALLUCINATION
   Never use outside knowledge.

3. FAILURE DEFAULT
   If the answer cannot be found in the Context,
   respond exactly:

   No Answer in the Given Documents

4. CITATIONS
   Mention file names if relevant.

[SOURCE CONTEXT]

{text}

[USER QUESTION]

{query}

[ANSWER]
""",
    input_variables=["text", "query"]
)

parser = StrOutputParser()

def ask_question(chat_id, query):
    
    records, _ = client.scroll(
    collection_name=COLLECTION_NAME,
    limit=3,
    with_payload=True
)

    print("\n===== QDRANT PAYLOAD DEBUG =====")

    for record in records:
       print(record.payload)

    print("=================================\n")
    vector_store = get_vector_store()

    chat_filter = Filter(
    must=[
        FieldCondition(
            key="metadata.chat_id",
            match=MatchValue(
                value=chat_id
            )
        )
    ]
)
    
  

    docs = vector_store.similarity_search(
        query=query,
        k=5,
        filter=chat_filter
        
    )
    print("="*50)
    print("Retrieved Docs:", len(docs))

    for i, doc in enumerate(docs):
       print(f"\nDOC {i+1}")
       print(doc.metadata)
       print(doc.page_content[:300])
 
    if not docs:

        return "No Answer in the Given Documents"


    context_parts = []

    for doc in docs:

        file_name = doc.metadata.get(
            "file_name",
            "Unknown File"
        )

        context_parts.append(
            f"""
SOURCE FILE:
{file_name}

CONTENT:
{doc.page_content}
"""
        )

    context = "\n\n".join(
        context_parts
    )



    chain = (
        prompt
        | chat_model
        | parser
    )

    response = chain.invoke(
        {
            "text": context,
            "query": query
        }
    )

    return response