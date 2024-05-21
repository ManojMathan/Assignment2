import streamlit as st
import openai
from PyPDF2 import PdfReader


openai.api_key = 'YOUR_OPENAI_API_KEY'


# Function to read PDF and extract text
def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_response(query, document_text):
    
    chunks = document_text.split("\n\n")
    
    relevant_chunks = [chunk for chunk in chunks if query.lower() in chunk.lower()]
    
    context = "\n\n".join(relevant_chunks[:3])
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}\nAnswer:"}
        ]
    )
    return response.choices[0].message['content'].strip()


st.title("PDF Chatbot")
st.write("Upload a PDF file and ask questions about its content.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    document_text = read_pdf(uploaded_file)
    st.write("PDF content loaded. You can now ask questions about the PDF.")

    query = st.text_input("Ask a question about the PDF:")
    if query:
        response = generate_response(query, document_text)
        st.write("Response:")
        st.write(response)
