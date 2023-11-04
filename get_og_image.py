import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import argparse
import os

def get_og_data(url, timeout=2):
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        
        # Open Graph 이미지를 가져오거나 대체 이미지를 찾습니다.
        og_image = soup.find('meta', {'property': 'og:image'})
        if og_image and og_image.get('content'):
            image = urljoin(url, og_image['content'])
        else:
            first_image = soup.find('img')
            image = urljoin(url, first_image['src']) if first_image else None
        
        # Open Graph 타이틀을 가져오거나 대체 타이틀을 찾습니다.
        og_title = soup.find('meta', {'property': 'og:title'})
        if og_title and og_title.get('content'):
            title = og_title['content']
        else:
            page_title = soup.find('title')
            title = page_title.get_text() if page_title else None
        
        # Open Graph 설명을 가져옵니다.
        og_description = soup.find('meta', {'property': 'og:description'})
        description = og_description['content'] if og_description else None

        return {
            'image': image,
            'title': title,
            'description': description
        }
    except Exception as e:
        print(f"Error for URL {url}: {e}")
        return None

def sanitize_url(url):
    return url.replace('.', '_').replace('https://', 'https_').replace('http://', 'http_').replace('/', '-').rstrip('/')

import re

# URL 패턴을 정의합니다.
url_pattern = re.compile(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+')

def process_urls(file_path):
    if not os.path.exists('data'):
        os.makedirs('data')

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # 파일 내용에서 URL 패턴에 해당하는 모든 문자열을 찾습니다.
        urls = re.findall(url_pattern, content)
        
        for url in urls:
            url=url.rstrip(")").rstrip("/")
            print(url)
            og_data = get_og_data(url)
            if og_data is not None:
                json_filename = sanitize_url(url) + '.json'
                with open(os.path.join('data', json_filename), 'w', encoding='utf-8') as json_file:
                    json.dump(og_data, json_file, ensure_ascii=False)
                print(f"Finished processing URL: {url}")
            else:
                print(f"Skipping URL {url} due to error.")
        print("All URLs have been processed.")

# 나머지 코드는 동일하게 유지합니다.


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get OG data from URLs listed in a file')
    parser.add_argument('file', help='The file containing URLs')
    args = parser.parse_args()

    process_urls(args.file)
    print("Script completed.")