import streamlit as st
import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client_ai = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

client_db = chromadb.PersistentClient(path="./chroma_db")
collection = client_db.get_or_create_collection(name="resume")


def ask_resume(question):
    results = collection.query(
        query_texts=[question],
        n_results=3
    )
    relevant_chunks = results["documents"][0]
    context = "\n\n".join(relevant_chunks)

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


# --- This is the new part: the actual web interface ---

st.title("Ask My Resume")
st.write("Ask any question about my background and experience.")

question = st.text_input("Your question:")

if question:
    answer = ask_resume(question)
    st.write(answer)