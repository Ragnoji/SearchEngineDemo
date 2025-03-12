import requests
from time import sleep
import os

data = dict()
article_index = 669675
url_count = 0
urls = []

if not os.path.exists('htmls'):
    os.makedirs('htmls')
while url_count < 5:
    article_index -= 1
    url = f"https://habr.com/ru/articles/{article_index}"
    response = requests.get(url)
    if response.status_code != 200:
        sleep(0.5)
        continue
    url_count += 1
    html = response.text
    with open(f'htmls/{url_count}.html', 'w', encoding='utf-8') as f:
        f.writelines(html)
    urls.append(url)
    sleep(0.5)
with open('index.txt', 'w', encoding='utf-8') as f:
    f.writelines([f"{i} {urls[i]}\n" for i in range(len(urls))])
