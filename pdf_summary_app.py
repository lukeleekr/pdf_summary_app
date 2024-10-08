import streamlit as st
import summarize_text_AI
import openai
import os
from PyPDF2 import PdfReader
import tiktoken
import textwrap
# Adding custom CSS for reducing title size and spacing
st.markdown(
    """
    <style>
    .title {
        font-size: 32px;
        color: #4CAF50;
        margin-top: -60px;
    }
    .subheader {
        font-size: 24px;
        color: #007BFF;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
    }
    .stFileUploader {
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)
# PDF 파일을 요약하는 함수
def summarize_pdf_file(pdf_file, lang, trans_checked):
    if pdf_file is not None:
        progress_text = st.empty() # Progress feedback
        progress_bar = st.progress(0) # Add progress bar
        
        reader = PdfReader(pdf_file)
        text_summaries = []
        
        for i, page in enumerate(reader.pages):
            progress_text.text(f"Processing page {i + 1}/{len(reader.pages)}...") 
            page_text = page.extract_text() # Extract text from each page
            text_summary = summarize_text_AI.summarize_text(page_text)
            text_summaries.append(text_summary)
            progress_bar.progress((i + 1) / len(reader.pages)) # Update progress bar
            
        token_num, final_summary = summarize_text_AI.summarize_text_final(text_summaries, lang)
        
        progress_bar.empty() # Clear the progress bar
        progress_text.empty() # Clear progress feedback
        
        if final_summary != "":
            st.success("Summary complete!")
            st.write(f"**Final Summary:** {final_summary}")
            
            # Translation handling
            if trans_checked:
                ko_summary = summarize_text_AI.translate_en_to_ko_using_deepl(final_summary)
                st.write(f"**Korean Summary:** {ko_summary}")
            
            # Download option for the summary
            st.download_button(
                label="Download Summary",
                data=final_summary,
                file_name="summary.txt",
                mime="text/plain",
            )
        else:
            st.error("Document too lengthy to summarize.")
            
# Main Streamlit app
def main():
    st.title("📄 PDF Summarization and Translation Tool")
    st.subheader("Easily summarize PDF files and translate them!")
    
    # Sidebar inputs
    with st.sidebar:
        st.header("Upload & Settings")
        uploaded_file = st.file_uploader("📤 Upload a PDF file", type=["pdf"])
        radio_selected_lang = st.radio("Document Language", ["English", "Korean"], index=0)
        
        if radio_selected_lang == "English":
            lang = "en"
            trans_checked = st.checkbox("Include Korean Translation")
        else:
            lang = "ko"
            trans_checked = False
        
        clicked = st.button("Start Summarization")
    
    # Display uploaded file preview
    if uploaded_file:
        with st.expander("Preview Uploaded PDF"):
            reader = PdfReader(uploaded_file)
            first_page_text = reader.pages[0].extract_text()
            st.write(first_page_text[:500])  # Show a snippet of the first page

    # Summarization process
    if clicked:
        if uploaded_file:
            summarize_pdf_file(uploaded_file, lang, trans_checked)
        else:
            st.error("Please upload a PDF file.")

if __name__ == "__main__":
    main()