import urllib.request
from bs4 import BeautifulSoup
import json
import argparse

def get_og_data(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        og_image = soup.find('meta', {'property': 'og:image'})
        og_title = soup.find('meta', {'property': 'og:title'})
        og_description = soup.find('meta', {'property': 'og:description'})

        return {
            'image': og_image['content'] if og_image else None,
            'title': og_title['content'] if og_title else None,
            'description': og_description['content'] if og_description else None
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get OG data from URL')
    parser.add_argument('url', help='The URL to fetch OG data from')
    args = parser.parse_args()

    og_data = get_og_data(args.url)
    json_filename = args.url.replace('.', '_').replace('https://', 'https_').replace('http://', 'http_') + '.json'

    with open(f'data/{json_filename}', 'w') as json_file:
        json.dump(og_data, json_file)
