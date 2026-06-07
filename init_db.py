from db import get_connection

conn = get_connection()

cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS chats(

        chat_id TEXT PRIMARY KEY,

        title TEXT,

        created_at TIMESTAMP DEFAULT NOW()
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS messages(

        id SERIAL PRIMARY KEY,

        chat_id TEXT,

        role TEXT,

        content TEXT,

        created_at TIMESTAMP DEFAULT NOW()
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS documents(

        id SERIAL PRIMARY KEY,

        chat_id TEXT,

        file_name TEXT,

        uploaded_at TIMESTAMP DEFAULT NOW()
    )
    """
)

conn.commit()

conn.close()

print("Database Ready")