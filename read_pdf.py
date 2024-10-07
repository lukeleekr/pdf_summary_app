from PyPDF2 import PdfReader

reader = PdfReader("Learn AI Assisted Programming/Learn_AI-Assisted_Python_Programming.pdf")
meta = reader.metadata # pdf 문서의 메타데이터 가져옴 (제목, 작가 등)
page = reader.pages[0] # n(정수)를 통해 n+1 페이지의 내용을 가져옴. n은 0부터 시작
page_text = page.extract_text() # 페이지의 텍스트 추출

print("- 문서 제목: ", meta.title)
print("- 문서 작가: ", meta.author)
print("- 첫 페이지 내용 일부:\n", page_text[0:300])
