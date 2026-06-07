We are gonna be using metadata filtering. 

How does chatGpt take multiple documents for every chat? When i access chat A (which contains X documents) or when i access chat B (which contains Y documents) the query which i ask in chat A might contains some words or info from chat B but does not give answer in context to the Chat B and same goes while working with chat B does not give answer in context of A. What is the database structure that is followed. How are the embeddings stored. 

User
  |
  v
Chat Service
  |
  +---- Message DB
  |
  +---- Document Store (S3)
  |
  +---- Vector DB
            |
            +-- chunk
            +-- embedding
            +-- chat_id
            +-- document_id

JSON should have : 
chat_id
document_id
chunk_id
embedding
metadata            



Example:
use Qdrant

{
  "chat_id": "A",
  "document_id": "X",
  "chunk": "Revenue grew by 30%",
  "embedding": [0.123,-0.556,...]
}



docker run -p 6333:6333 qdrant/qdrant