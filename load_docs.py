# This let's me open the PDF file in Python 
from pypdf import PdfReader 

# Open the resume file 
reader = PdfReader("Evelis_Zapata's_Resume.pdf")

# Start with an empty piece of text (I'll fill it up next)
text = ""

#Go through the resume one page at a time 
for page in reader.pages: 

# Take the words from this page & add them to "text"
# After this loop ends, "text" = the whole resume as one long piece of text 
    text += page.extract_text()

#This is a function we're making. A function is just a set of steps we can reuse. 
# It takes the resume text & cuts it into smaller pieces ("chunks")
def chunk_text(text, chunk_size=500, overlap=50):

# An empty list to hold each small piece
    chunks = []

# This keeps track of where we are in the text. We start at the very beginning. 
    start = 0

#Keep going until we covered the whole text. 
    while start < len(text):
# Where this piece should stop (500 characters later)
        end = start + chunk_size
# Cut out that piece of text & save it
        chunks.append(text[start:end])
# Move forward with the next piece
# We go back a little (overlap) so we don't cut off a sentence in the middle 
        start += chunk_size - overlap
# Give back the full list of small pieces 
    return chunks

# Actually run the function on my resume text
chunks = chunk_text(text)

# Show how many pieces we ended up with
print(f"Number of chunks: {len(chunks)}")

# Show the very first piece, just to check it looks right 
print("First chunk:")
print(chunks[0])