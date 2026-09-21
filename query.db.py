import chromadb

# Connect to the same database we already created
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="resume")

# The question we want to ask about the resume 
question = "What cloud experience does she have?"

# Ask chroma to find the most relevant chunks for this information 
results = collection.query(
    query_texts=[question], 
    n_results=3
)

# Print out the chunks it found 
for chunk in results["documents"][0]:
    print(chunk)
    print("---")
    