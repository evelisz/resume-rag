# chromadb is the database that stores our chunks so we can search them later
from pypdf import PdfReader
import chromadb

# Open the resume file (same as before)
reader = PdfReader("Evelis_Zapata's_Resume.pdf")

text = ""
# Start with an empty piece of text (we'll fill it up next)

# Same as before - get all the resume text in one piece
for page in reader.pages:
    text += page.extract_text()

# Same chunking function as before - no changes here
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# Cut the resume into small pieces - same as before
chunks = chunk_text(text)

# Creates a database that saves to a folder called "chroma_db"
# "Persistent" means it stays saved even after we close the program
client = chromadb.PersistentClient(path="./chroma_db")

# Inside the database make a labeled section just for the resume chunks
# Think of this like a folder inside the database, named "resume"
collection = client.get_or_create_collection(name="resume")

# Store every chunk in the database
# Each chunk needs a unique name/ID, so we make them: chunk_0, chunk_1, chunk_2, etc.
# Chroma automatically turns each chunk into "meaning numbers" behind the scenes,
# so it can later find chunks by what they MEAN, not just exact words
collection.add(
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

# Just checking - print how many chunks actually got saved
print(f"Stored {collection.count()} chunks in the database.")