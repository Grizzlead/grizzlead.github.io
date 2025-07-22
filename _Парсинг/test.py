# --- 1 Вариант ---

# import requests

# headers = {
#     'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
# }

# session = requests.Session()

# req = session.get('https://www.dotabuff.com/matches/8378959607', headers=headers)
# print(req.status_code)

# --- 2 Вариант ---

# import cfscrape

# scrapper = cfscrape.create_scraper()
# response = scrapper.get(r'https://www.dotabuff.com/matches/8378959607')

# print(response.status_code)

# --- 3 Вариант (Тихий режим)---

# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver

# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)

# driver.get(url="https://www.dotabuff.com/matches/8378959607")
# page_source = driver.page_source

# with open('page.html', 'w', encoding='utf-8') as file:
#     file.write(page_source)

# driver.quit()

# --- 4 Вариант (Тихий режим)---

# from selenium import webdriver

# driver = webdriver.Chrome()

# driver.get(url="https://www.dotabuff.com/matches/8378959607")
# page_source = driver.page_source

# with open('page.html', 'w', encoding='utf-8') as file:
#     file.write(page_source)

# driver.quit()

# --- 5 Вариант (Итог)---

from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()

driver.get(url="https://www.dotabuff.com/matches/8378959607")
page_source = driver.page_source

soup_main = BeautifulSoup(page_source, 'lxml')

driver.quit()

# 1. Teams
team_radiant = soup_main.select_one('.team-results .radiant header .team-text-full').text
team_dire = soup_main.select_one('.team-results .dire header .team-text-full').text
teams = {'Radiant':team_radiant, 'Dire':team_dire}
print(team_radiant, team_dire)