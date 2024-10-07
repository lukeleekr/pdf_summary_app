import streamlit as st
import summarize_text_AI
import openai
import os
from PyPDF2 import PdfReader
import tiktoken
import textwrap

# PDF 파일을 요약하는 함수
def summarize_pdf_file(pdf_file, lang, trans_checked):
    if pdf_file is not None:
        st.write("PDF 문서를 요약 중입니다. 잠시만 기다려 주세요.")
        reader = PdfReader(pdf_file) # PDF 문서 읽기
        text_summaries = []
        for page in reader.pages:
            page_text = page.extract_text() # 페이지의 텍스트를 추출
            text_summary = summarize_text_AI.summarize_text(page_text)
            text_summaries.append(text_summary)
        token_num, final_summary = summarize_text_AI.summarize_text_final(text_summaries, lang)

        if final_summary != "":
            st.write(f"- 최종 요약: {final_summary}")
            if trans_checked:
                ko_summary = summarize_text_AI.translate_en_to_ko_using_deepl(final_summary)
                st.write(f"- 한국어 요약: {ko_summary}")
        else:
            st.write("- 요약하려는 문서의 길이 초과로 인해 요약할 수 없습니다.")

# Streamlit 애플리케이션 실행
def main():
    st.title("PDF 문서 요약 애플리케이션")
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요.", type=["pdf"])
    radio_selected_lang = st.radio("PDF 문서 언어", ["영어", "한국어"], index=0, horizontal=True)
    if radio_selected_lang == "영어":
        lang = "en"
        checked = st.checkbox("한국어 번역 추가")
    else:
        lang = "ko"
        checked = False
    clicked = st.button("PDF 문서 요약하기")
    if clicked:
        summarize_pdf_file(uploaded_file, lang, checked)

if __name__ == "__main__":
    main()
