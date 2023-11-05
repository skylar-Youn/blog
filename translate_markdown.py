import requests
import json
import sys
import configparser
# OpenAI API 설정
config = configparser.ConfigParser()
# DeepL API URL 및 인증 키
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_AUTH_KEY =  config['DEFAULT']['DEEPL_API_KEY']

# 번역할 대상 언어 설정 (예: 독일어 'DE')
TARGET_LANG = "JA"

def translate_text(text, target_lang):
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_AUTH_KEY}",
        "User-Agent": "YourApp/1.2.3",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(DEEPL_API_URL, headers=headers, json=data)
    return response.json()

def translate_markdown_file(file_path, target_lang):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 문단 단위로 콘텐츠를 나눈다.
        paragraphs = content.split('\n\n')

        translated_paragraphs = []
        for paragraph in paragraphs:
            # 공백이 아닌 문단만 번역한다.
            if paragraph.strip():
                # 번역 API 호출
                translation_result = translate_text([paragraph], target_lang)
                translations = translation_result.get("translations", [])
                if translations:
                    translated_text = translations[0].get("text", "")
                    translated_paragraphs.append(translated_text)
                else:
                    # 번역 결과가 없으면 원본 텍스트를 사용
                    translated_paragraphs.append(paragraph)
            else:
                # 공백 문단은 그대로 유지
                translated_paragraphs.append(paragraph)
        
        # 번역된 마크다운 파일 생성
        translated_file_path = file_path.replace(".md", f"_{target_lang}.md")
        with open(translated_file_path, 'w', encoding='utf-8') as file:
            # 문단 사이에 두 개의 줄바꿈을 추가하여 원본 구조를 유지한다.
            file.write('\n\n'.join(translated_paragraphs))
        
        print(f"Translated markdown file created: {translated_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# 스크립트 실행
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python translate_markdown.py [path_to_markdown_file]")
    else:
        markdown_file_path = sys.argv[1]
        translate_markdown_file(markdown_file_path, TARGET_LANG)
