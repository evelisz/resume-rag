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
    return response.content[0].text, relevant_chunks


def highlight_chunks(full_text, chunks_to_highlight):
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

    # Wrap the resume in a scrollable, bordered box so messy PDF spacing
    # doesn't sprawl across the whole page
    st.markdown(
        f'''<div style="max-height: 500px; overflow-y: scroll; padding: 15px;
        border: 1px solid #ddd; border-radius: 8px; white-space: pre-wrap;
        font-family: monospace;">{highlighted_resume}</div>''',
        unsafe_allow_html=True
    )