import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

#print(UserAgent().chrome)

# with open('aspects.html', 'w', encoding='utf-8') as file:
#     headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36'}
#     data = requests.get('https://ru.dotabuff.com/heroes', headers=headers)
#     info_aspects = BeautifulSoup(data.text, 'lxml')
#     aspects = info_aspects.select('tr.tw-border-b')
#     for aspect in aspects:
#         file.write(str(aspect))

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36'}
# data = requests.get('https://ru.dotabuff.com/heroes', headers=headers)
with open('aspects.html', 'r', encoding='utf-8') as file:
    data = file.read()
info_aspects = BeautifulSoup(data, 'lxml')
aspects = info_aspects.select('tbody tr.tw-border-b.tw-transition-colors')

for aspect in aspects:
    print(' '.join(aspect.select('div.tw-gap-0 a')[0].text.split()).ljust(20), end=' ')
    print(' '.join(aspect.select('div.tw-gap-0 .tw-text-xs.tw-text-secondary')[0].text.split()).ljust(25), end=' ')
    print(aspect.select('.tw-rounded')[0].text.strip().ljust(5), end=' ')
    for item in aspect.select('.tw-p-2 span'):
        print(item.text.strip().ljust(10), end=' ')
    print()