import os
import pdfplumber
import streamlit as st
from groq import Groq
from fpdf import FPDF

# Initialize the Groq client with the API key from environment variable
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Streamlit app
st.image("p0.png", width=280)
st.title("Welcome to trans-text GChat AI")

# Sidebar
st.sidebar.title("Query Box")

# System prompt input in the sidebar
system_prompt = st.sidebar.text_area("Enter system prompt (optional):", value="", height=100)

# User prompt input in the sidebar
prompt = st.sidebar.text_area("Enter your prompt:", value="", height=150)

# File upload input in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload a text or PDF file", type=["txt", "pdf"])

# Function to read the contents of the uploaded text file
def read_uploaded_text(file):
    return file.read().decode("utf-8")

# Function to read the contents of the uploaded PDF file
def read_uploaded_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Read the content of the uploaded file, if any
file_content = ""
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        file_content = read_uploaded_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        file_content = read_uploaded_text(uploaded_file)

# Function to query Groq API
def query_groq(system_prompt, combined_prompt):
    try:
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt,
            })
        messages.append({
            "role": "user",
            "content": combined_prompt,
        })
        
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to save the reply as a PDF
def save_as_pdf(reply_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in reply_text.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output("translated_text.pdf")
    st.success("The translation has been saved as 'translated_text.pdf'")

# Button to submit the query
if st.sidebar.button("Submit"):
    if prompt or file_content:
        with st.spinner("Querying the chatbot..."):
            # Combine file content and user prompt
            combined_prompt = f"{file_content}\n{prompt}"
            # Query Groq's API
            reply = query_groq(system_prompt, combined_prompt)
            if reply:
                st.success("Query completed!")
                st.info(reply)
                
                # Option to save the response as a PDF
                if st.button("Save as PDF"):
                    save_as_pdf(reply)
            else:
                st.error("No response found.")
    else:
        st.sidebar.warning("Please enter a prompt or upload a file.")

# Reset button
if st.sidebar.button("Reset"):
    st.experimental_rerun()

# Instructions
st.write("Enter a system prompt (optional) and a user prompt in the sidebar, then click 'Submit' to get a response from the LLM.")
st.write("Alternatively, you can upload a text or PDF file to use its content as the prompt.")
st.write("Model: llama3-8b-8192")


st.info("build by DW v1 8-19-24") #v1
st.warning("format - translate text ")
st.image("p1.png")
st.image("p2.png")