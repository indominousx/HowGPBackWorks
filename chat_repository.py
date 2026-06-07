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