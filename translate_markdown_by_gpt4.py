import openai
import configparser
# OpenAI API 설정
config = configparser.ConfigParser()
 
# 설정 파서 생성# 'DEFAULT' 섹션에서 'API_KEY' 가져오기
api_key = config['DEFAULT']['OPENAI_API_KEY']
openai.api_key =api_key
# 설정 파일 읽기
config.read('config.ini')
def translate_with_chatgpt(text, source_lang="en", target_lang="es"):
    try:
        # 번역 요청
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # GPT-4의 모델을 지정
            prompt=f"Translate the following text from {source_lang} to {target_lang}:\n\n{text}",
            temperature=0.3,
            max_tokens=1024
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def translate_markdown_file(file_path, source_lang, target_lang):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        paragraphs = content.split('\n\n')
        translated_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                translated_text = translate_with_chatgpt(paragraph, source_lang, target_lang)
                translated_paragraphs.append(translated_text)
            else:
                translated_paragraphs.append(paragraph)
        
        translated_file_path = file_path.replace(".md", f"_{target_lang}.md")
        with open(translated_file_path, 'w', encoding='utf-8') as file:
            file.write('\n\n'.join(translated_paragraphs))
        
        print(f"Translated markdown file created: {translated_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# 스크립트 실행
if __name__ == "__main__":
    markdown_file_path = 'content/posts/awesome_article/index.en.md'  # 번역할 마크다운 파일 경로
    source_language = "en"  # 원본 언어 코드
    target_language = "ko"  # 목표 언어 코드
    translate_markdown_file(markdown_file_path, source_language, target_language)
