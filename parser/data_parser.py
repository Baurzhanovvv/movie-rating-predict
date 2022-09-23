import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


links = []
data = []

with open(r'links.txt', 'r') as r:
	for link in r:
		x = link[:len(link)-2]
		links.append(x)

def get_data(links, list):
	for link in links:
		page = requests.get(link)

		soup = bs(page.text, 'html.parser')

		data = {
			"title": soup.findAll('h1', class_='sc-b73cd867-0')[0].text,
			"year": soup.findAll('a', class_='ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh')[0].text,
			"certificate": soup.findAll('span', class_='sc-8c396aa2-2 itZqyK')[0].text,
			"rating": soup.findAll('span', class_='sc-7ab21ed2-1 jGRxWM')[0].text,
			"description": soup.findAll('span', class_='sc-16ede01-2 gXUyNh')[0].text,
			"director": soup.select('li.ipc-metadata-list__item:first-child > div > ul > li > a')[0].text,
			"writer": [soup.findAll('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')[0].text,
			soup.findAll('a',class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')[1].text],
			"actors": [soup.findAll('a', class_='sc-36c36dd0-1 QSQgP')[i].text for i in range(len(soup.findAll('a', class_='sc-36c36dd0-1 QSQgP')))],
			"genres": [soup.findAll('a', class_='ipc-chip__text')[i].text for i in range(len(soup.findAll('a', class_='ipc-chip__text')))],
			"runtime": soup.findAll('div', class_='ipc-metadata-list-item__content-container')[0].text,
		}

		list.append(data)
	return list


data = get_data(links, data)

films_df = pd.DataFrame(data)
films_df.to_csv('data.csv')
