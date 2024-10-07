import openai
import os
import tiktoken
import deepl

def summarize_text(user_text, lang='en'):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Define the system and user messages based on language
    if lang == 'en':
        system_message = "You are a helpful assistant that summarizes texts into detailed and comprehensive summaries. Remember you are summarizing a text for a very young audience, so your English has to be simple and easy to understand."
        user_message = f"Please provide a detailed summary of the following text:\n{user_text}"
    elif lang == 'ko':
        system_message = "당신은 텍스트를 상세하고 포괄적인 요약으로 요약하는 도움이 되는 어시스턴트입니다. 매우 어린 독자를 위해 텍스트를 요약하므로 한국어가 간단하고 이해하기 쉬워야 합니다."
        user_message = f"다음 텍스트를 자세히 요약해주세요:\n{user_text}"
    else:
        raise ValueError("Unsupported language.")

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]

    model_max_tokens = 2000

    # Set a buffer to leave space for the response
    buffer = 100  # Adjust based on desired response length

    # Calculate the maximum tokens allowed for the response
    max_tokens_allowed = model_max_tokens - buffer

    # Generate the summary with adjusted max_tokens
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens_allowed,
        temperature=0.3,  # Adjust for creativity
        n=1
    )

    summary = response.choices[0].message.content
    return summary

# 요약 리스트를 최종적으로 요약하는 함수
def summarize_text_final(text_list,lang='en'):
    # 리스트를 연결해 하나의 요약 문자열로 통합
    joined_summary = " ".join(text_list)
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    token_num = len(enc.encode(joined_summary))

    req_max_token = 2000  # Note: This exceeds the model's limit

    if token_num > req_max_token:
        print("최대 토큰 수를 초과했습니다.")
    elif token_num < req_max_token:
        final_summary = summarize_text(joined_summary, lang=lang)
    
    return token_num, final_summary

def translate_en_to_ko_using_openAI(text):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    system_message = "You are a helpful assistant that translates English texts into Korean. Your Korean must be accurate and natural."
    user_message = f"Translate the following text into Korean:\n{text}"

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2000,
        temperature=0.3,
        n=1
    )
    assistant_response = response.choices[0].message.content
    return assistant_response

def translate_en_to_ko_using_deepl(text):
    auth_key = os.environ["DeepL_API_KEY"]
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang="KO") # 번역할 언어를 한국어로 지정
    return result.text