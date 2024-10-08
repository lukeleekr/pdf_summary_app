import streamlit as st
import summarize_text_AI
from PyPDF2 import PdfReader

# Adding custom CSS for animations and styling
st.markdown(
    """
    <style>
    /* Add a gradient background to the app */
    .reportview-container {
        background: linear-gradient(135deg, #f5f7fa 10%, #c3cfe2 100%);

    }

    /* Title font customization */
    .title {
        font-size: 3em;
        font-weight: bold;
        color: #ff6347;  /* Tomato color */
        text-align: center;
        animation: fadeInDown 1s;
    }

    /* Subheader font customization */
    .subheader {
        font-size: 1.5em;
        font-weight: lighter;
        color: #4682b4;  /* Steel blue color */
        text-align: center;
        margin-bottom: 30px;
        animation: fadeInUp 1.5s;
    }

    /* Simple animation for the title and subheader */
    @keyframes fadeInDown {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Button customization */
    .stButton>button {
        background-color: #4CAF50;  /* Green background */
        color: white;
        font-size: 1.2em;
        border-radius: 8px;
        padding: 10px 20px;
        margin-top: 10px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;  /* Darker green on hover */
    }

    </style>
    """, unsafe_allow_html=True
)

# PDF summarization function
def summarize_pdf_file(pdf_file, lang, trans_checked):
    if pdf_file is not None:
        st.write("📄 Summarizing the PDF document... please wait.")
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        reader = PdfReader(pdf_file)
        text_summaries = []
        
        for i, page in enumerate(reader.pages):
            progress_text.text(f"🔄 Processing page {i + 1}/{len(reader.pages)}...")
            page_text = page.extract_text()  # Extract text from each page
            text_summary = summarize_text_AI.summarize_text(page_text)
            text_summaries.append(text_summary)
            progress_bar.progress((i + 1) / len(reader.pages))  # Progress bar animation
            
        token_num, final_summary = summarize_text_AI.summarize_text_final(text_summaries, lang)
        
        progress_bar.empty()
        progress_text.empty()
        
        if final_summary != "":
            st.success("✅ Summarization complete!")
            st.write(f"**Final Summary:** {final_summary}")
            
            # Translation handling
            if trans_checked:
                ko_summary = summarize_text_AI.translate_en_to_ko_using_deepl(final_summary)
                st.write(f"**Korean Summary:** {ko_summary}")
            
            # Option to download the summary
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
    # Title with custom animation and styling
    st.markdown('<h1 class="title">📄 Summarize your PDF!</h1>', unsafe_allow_html=True)
    
    # Subheader with animation and lighter text
    st.markdown('<h3 class="subheader">Easily summarize PDF files and translate them!</h3>', unsafe_allow_html=True)

    # Sidebar inputs
    with st.sidebar:
        st.header("Upload & Settings")
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        radio_selected_lang = st.radio("Document Language", ["English", "Korean"], index=0)
        
        if radio_selected_lang == "English":
            lang = "en"
            trans_checked = st.checkbox("Include Korean Translation")
        else:
            lang = "ko"
            trans_checked = False
        
        clicked = st.button("Summarize PDF")

    # Display uploaded file preview
    if uploaded_file:
        with st.expander("Preview Uploaded PDF"):
            reader = PdfReader(uploaded_file)
            first_page_text = reader.pages[0].extract_text()
            st.write(first_page_text[:500] + "...[생략]")   # Show a snippet of the first page

    # Summarization process
    if clicked:
        if uploaded_file:
            summarize_pdf_file(uploaded_file, lang, trans_checked)
        else:
            st.error("Please upload a PDF file.")

    # Footer at the bottom
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: transparent;
            color: grey;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
        </style>
        <div class="footer">
            <p>Created by 동나의 욘노니~!</p>
        </div>
        """, unsafe_allow_html=True)
if __name__ == "__main__":
    main()
