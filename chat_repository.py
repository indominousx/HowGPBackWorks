from db import get_connection


def create_chat(
    chat_id,
    title="New Chat"
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO chats(
            chat_id,
            title
        )
        VALUES(%s,%s)
        """,
        (
            chat_id,
            title
        )
    )

    conn.commit()

    conn.close()

def get_all_chats():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            chat_id,
            title
        FROM chats
        ORDER BY created_at DESC
        """
    )

    rows = cur.fetchall()

    conn.close()

    return rows 


def save_message(
    chat_id,
    role,
    content
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO messages(
            chat_id,
            role,
            content
        )
        VALUES(%s,%s,%s)
        """,
        (
            chat_id,
            role,
            content
        )
    )

    conn.commit()

    conn.close()

def get_messages(
    chat_id
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            role,
            content
        FROM messages
        WHERE chat_id=%s
        ORDER BY id
        """,
        (chat_id,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows

def update_chat_title(
    chat_id,
    title
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE chats
        SET title=%s
        WHERE chat_id=%s
        """,
        (
            title,
            chat_id
        )
    )

    conn.commit()

    conn.close()   

def get_chat_title(
    chat_id
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT title
        FROM chats
        WHERE chat_id=%s
        """,
        (chat_id,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return None     

def update_chat_title(
    chat_id,
    title
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE chats
        SET title=%s
        WHERE chat_id=%s
        """,
        (
            title,
            chat_id
        )
    )

    conn.commit()

    conn.close()


def save_document(
    chat_id,
    file_name
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO documents(
            chat_id,
            file_name
        )
        VALUES(%s,%s)
        """,
        (
            chat_id,
            file_name
        )
    )

    conn.commit()

    conn.close()    


def get_documents(
    chat_id
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT file_name
        FROM documents
        WHERE chat_id=%s
        ORDER BY uploaded_at DESC
        """,
        (chat_id,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows


def document_exists(
    chat_id,
    file_name
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT 1
        FROM documents
        WHERE chat_id=%s
        AND file_name=%s
        LIMIT 1
        """,
        (
            chat_id,
            file_name
        )
    )

    row = cur.fetchone()

    conn.close()

    return row is not None