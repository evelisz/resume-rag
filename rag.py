import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client_ai = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Connect to our existing database
client_db = chromadb.PersistentClient(path="./chroma_db")
collection = client_db.get_or_create_collection(name="resume")


def ask_resume(question):
    # Step 1: Find the most relevant chunks for this question
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    relevant_chunks = results["documents"][0]

    # Step 2: Combine the chunks into one block of context
    context = "\n\n".join(relevant_chunks)

    # Step 3: Ask Claude to answer using ONLY that context
    response = client_ai.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"""Answer the question using only the resume excerpts below.
If the answer isn't in the excerpts, say so.

Resume excerpts:
{context}

Question: {question}"""
            }
        ]
    )

    return response.content[0].text


# Try it out
answer = ask_resume("What cloud experience does she have?")
print(answer)