from selenium import webdriver
from bs4 import BeautifulSoup


# membuat driver headless
options = webdriver.ChromeOptions()

options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)

# Link target
driver.get('https://www.bola.net/indonesia/')
content = driver.page_source

content_soup = BeautifulSoup(content,"html.parser")

data_main = content_soup.find('div', class_='main')
data_class = data_main.find('ul', class_='box-article-list list-unstyled')
data_title = data_class.find_all('a')
for list in data_title:
    list_title = list.get_text()
    print(list_title)




