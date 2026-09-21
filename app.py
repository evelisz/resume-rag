import streamlit as st
import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv
import os
from pypdf import PdfReader

load_dotenv()
client_ai = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

client_db = chromadb.PersistentClient(path="./chroma_db")
collection = client_db.get_or_create_collection(name="resume")


# Load the full resume text once, so we can display it and highlight parts of it later
reader = PdfReader("Evelis_Zapata's_Resume.pdf")
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()


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
    # Return BOTH the answer and the chunks used, since we need the chunks to highlight later
    return response.content[0].text, relevant_chunks


def highlight_chunks(full_text, chunks_to_highlight):
    # Take the full resume text, and wrap any part that matches a used chunk
    # in a yellow highlight (using basic HTML, since Streamlit can render HTML)
    highlighted = full_text
    for chunk in chunks_to_highlight:
        if chunk in highlighted:
            highlighted = highlighted.replace(
                chunk,
                f'<mark style="background-color: #FFF176;">{chunk}</mark>'
            )
    return highlighted


# --- Web interface ---

st.title("Ask My Resume")
st.write("Ask any question about my background and experience.")

question = st.text_input("Your question:")

if question:
    answer, used_chunks = ask_resume(question)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Resume (highlighted sections were used to answer your question)")
    highlighted_resume = highlight_chunks(full_text, used_chunks)
    st.markdown(highlighted_resume, unsafe_allow_html=True)