import streamlit as st
import requests
import os

# Set up the Streamlit app
st.set_page_config(page_title="NotesAI", layout="wide")

# Title
st.title("NotesAI: AI-Powered Note-Taking Application")

# File Upload Section
st.header("Upload Audio or PDF")
uploaded_file = st.file_uploader("Upload an audio or PDF file", type=["mp3", "wav", "ogg", "pdf"])

if uploaded_file:
    # Save the uploaded file temporarily
    temp_file_path = os.path.join("storage", "temp", uploaded_file.name)
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File uploaded successfully: {uploaded_file.name}")

    # Select processing type
    processing_type = st.radio("Select Processing Type", ["Transcription", "PDF Parsing"])

    if st.button("Process File"):
        if processing_type == "Transcription":
            # Call the transcription API
            with st.spinner("Processing transcription..."):
                response = requests.post(
                    "http://localhost:5000/transcribe",
                    files={"file": open(temp_file_path, "rb")}
                )
                if response.status_code == 200:
                    transcription = response.json().get("transcription", "")
                    st.subheader("Transcription")
                    st.text_area("Transcribed Text", transcription, height=200)
                else:
                    st.error("Failed to process transcription.")
        elif processing_type == "PDF Parsing":
            # Call the PDF parsing API
            with st.spinner("Extracting text from PDF..."):
                response = requests.post(
                    "http://localhost:5000/extract_pdf",
                    files={"file": open(temp_file_path, "rb")}
                )
                if response.status_code == 200:
                    extracted_text = response.json().get("text", "")
                    st.subheader("Extracted Text")
                    st.text_area("Extracted Text from PDF", extracted_text, height=200)
                else:
                    st.error("Failed to extract text from PDF.")

# Summarization Section
st.header("Summarization")
input_text = st.text_area("Enter text to summarize")
summary_method = st.radio("Select Summarization Method", ["Abstractive", "Extractive"])
summary_length = st.selectbox("Select Summary Length", ["Short", "Medium", "Long"])

if st.button("Summarize Text"):
    if input_text:
        with st.spinner("Generating summary..."):
            response = requests.post(
                "http://localhost:5000/summarize",
                json={"transcription": input_text, "method": summary_method.lower(), "length": summary_length.lower()}
            )
            if response.status_code == 200:
                summary = response.json().get("summary", "")
                st.subheader("Summary")
                st.text_area("Generated Summary", summary, height=150)
            else:
                st.error("Failed to generate summary.")
    else:
        st.warning("Please enter text to summarize.")

# Keyword Extraction Section
st.header("Keyword Extraction")
if st.button("Extract Keywords"):
    if input_text:
        with st.spinner("Extracting keywords..."):
            response = requests.post(
                "http://localhost:5000/extract_keywords",
                json={"text": input_text, "method": "spacy"}
            )
            if response.status_code == 200:
                keywords = response.json().get("keywords", [])
                st.subheader("Extracted Keywords")
                for keyword in keywords:
                    st.write(f"- {keyword['keyword']} (Score: {keyword['score']:.2f})")
            else:
                st.error("Failed to extract keywords.")
    else:
        st.warning("Please enter text to extract keywords.")

# Notes Management Section
st.header("Manage Notes")
if st.button("Fetch Notes"):
    with st.spinner("Fetching notes..."):
        response = requests.get("http://localhost:5000/notes")
        if response.status_code == 200:
            notes = response.json().get("notes", [])
            for note in notes:
                st.subheader(note["title"])
                st.write(f"**Transcription:** {note['transcription']}")
                st.write(f"**Summary:** {note['summary']}")
                st.write(f"**Quiz:** {note['quiz']}")
        else:
            st.error("Failed to fetch notes.")
