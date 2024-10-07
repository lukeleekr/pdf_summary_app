from PyPDF2 import PdfReader
import tiktoken
from summarize_text_AI import summarize_text, summarize_text_final, translate_en_to_ko_using_openAI, translate_en_to_ko_using_deepl

# Check the current address
pdf_file = "/Users/lukeylee/Desktop/CS/API_book/President Obamas Farewell Address (TRANSCRIPT).pdf"
reader = PdfReader(pdf_file)

enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
"""
page_token_nums = []
for page in reader.pages:
    page_text = page.extract_text() # 페이지의 텍스트를 추출
    token_num = len(enc.encode(page_text)) # 페이지의 토큰 수를 계산
    page_token_nums.append(token_num) # 페이지의 토큰 수를 리스트에 추가

print("각 페이지의 토큰 수", page_token_nums)
print("전체 페이지에서 최대 토큰 수", max(page_token_nums))
print("전체 페이지의 토큰 수 합계", sum(page_token_nums))
"""
text_summaries = []
for page in reader.pages:
    page_text = page.extract_text()
    #print(f"페이지 토큰 수: {len(enc.encode(page_text))}")
    text_summary = summarize_text(page_text)
    text_summaries.append(text_summary)


token_num, final_summary = summarize_text_final(text_summaries)
en_text = final_summary
ko_text_openAI = translate_en_to_ko_using_openAI(en_text)
ko_text_deepl = translate_en_to_ko_using_deepl(en_text)
#print(f"- 최종 토큰 수: {token_num}\n")
print(f"- 최종 요약본 (영문): {en_text}\n")
print(f"- 최종 요약본 (한글)_OpenAI: {ko_text_openAI}\n")
print(f"- 최종 요약본 (한글)_DeepL: {ko_text_deepl}\n")

