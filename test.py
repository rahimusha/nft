import csv

import requests
from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

FILE = 'nft.csv'

driver = webdriver.Chrome(executable_path='./chromedriver')

driver.get("https://opensea.io/collection/justinaversano-gabbagallery?tab=activity")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

items = soup.findAll('div', attrs={"class":"Blockreact__Block-sc-1xf18x6-0 styles__CoverLinkContainer-sc-nz4knd-2 elqhCm hguuhN"})

nft = []
for item in items:
    nft.append({
        'title': item.find('div', class_='Overflowreact__OverflowContainer-sc-7qr9y8-0 jRbcys').get_text(),
        'price': item.find('div', class_='Overflowreact__OverflowContainer-sc-7qr9y8-0 jPSCbX Price--fiat-amount').get_text()

    })

for item in nft:
    print(nft)


def save_file(item, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['NFT name', 'price in dollar'])
        for item in nft:
            writer.writerow([item['title'], item['price']])


save_file(nft, FILE)











