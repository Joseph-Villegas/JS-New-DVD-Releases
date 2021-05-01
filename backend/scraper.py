import requests
from bs4 import BeautifulSoup

def scrape():
	url = 'https://www.dvdsreleasedates.com'
	response = requests.get(url)
	soup = BeautifulSoup(response.content, features="lxml")

	tables = soup.findAll(attrs={'class': 'fieldtable-inner'})

	scrape_results = []
	for table in tables:
		release_week = table.find(attrs={'class': 'reldate'})
		print(f'Release Week Info: {release_week.text}')


		imdb_ids = [tag.find('a').attrs['href'].split('/')[4] for tag in table.findAll(attrs={'class': 'imdblink left'})]

		movies = []
		for dvd in table.findAll('img'):
			if 'src' in dvd.attrs and dvd.attrs['src'].endswith('jpg'):
				title = dvd.attrs['title'].replace(' DVD Release Date', '')
				poster = dvd.attrs['src']
				movies.append({'title': title, 'poster': poster})

		for movie, imdb_id in zip(movies, imdb_ids):
			movie['imdb_id'] = imdb_id

		scrape_results.append({'release_week': release_week.text, 'movies': movies, 'num_movies': len(movies)})

	return scrape_results

def search_by_week(query):
	return [result for result in scrape() if query in result['release_week']]