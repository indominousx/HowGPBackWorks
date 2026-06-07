import os
import uuid

import streamlit as st

from documentloader import get_pdf_chunks
from genembeddings import ingest_documents
from rag_chain import ask_question

from chat_repository import (
    create_chat,
    get_all_chats,
    get_messages,
    save_message
)


st.set_page_config(
    page_title="Enterprise Document Chatbot",
    page_icon="📄",
    layout="wide"
)

st.title("Enterprise Document Chatbot")


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

if "chat_id" not in st.session_state:

    new_chat_id = uuid.uuid4().hex

    create_chat(
        new_chat_id
    )

    st.session_state.chat_id = (
        new_chat_id
    )

chat_id = st.session_state.chat_id



with st.sidebar:

    st.title("Chats")

    if st.button("➕ New Chat"):

        new_chat_id = (
            uuid.uuid4().hex
        )

        create_chat(
            new_chat_id
        )

        st.session_state.chat_id = (
            new_chat_id
        )

        st.rerun()

    st.divider()

    chats = get_all_chats()

    for chat_row in chats:

        current_chat_id = chat_row[0]
        title = chat_row[1]

        if st.button(
            title,
            key=current_chat_id
        ):

            st.session_state.chat_id = (
                current_chat_id
            )

            st.rerun()



st.subheader(
    f"Chat ID: {chat_id[:8]}"
)



uploaded_files = st.file_uploader(
    "Upload PDF Documents",
    type=["pdf"],
    accept_multiple_files=True
)



if st.button("Process Documents"):

    if not uploaded_files:

        st.warning(
            "Please upload at least one PDF."
        )

    else:

        chat_folder = os.path.join(
            UPLOAD_DIR,
            chat_id
        )

        os.makedirs(
            chat_folder,
            exist_ok=True
        )

        file_paths = []

        for file in uploaded_files:

            save_path = os.path.join(
                chat_folder,
                file.name
            )

            with open(
                save_path,
                "wb"
            ) as f:

                f.write(
                    file.getbuffer()
                )

            file_paths.append(
                save_path
            )

        with st.spinner(
            "Loading PDFs..."
        ):

            chunks = get_pdf_chunks(
                file_paths=file_paths,
                chat_id=chat_id
            )

            ingest_documents(
                chunks
            )

        st.success(
            f"{len(file_paths)} documents indexed."
        )



messages = get_messages(
    chat_id
)

for role, content in messages:

    with st.chat_message(
        role
    ):

        st.markdown(
            content
        )



query = st.chat_input(
    "Ask a question..."
)

if query:



    save_message(
        chat_id=chat_id,
        role="user",
        content=query
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            query
        )


    with st.spinner(
        "Searching Documents..."
    ):

        answer = ask_question(
            chat_id=chat_id,
            query=query
        )

    save_message(
        chat_id=chat_id,
        role="assistant",
        content=answer
    )

    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            answer
        )

    st.rerun()