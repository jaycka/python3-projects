import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())

movies = soup.find_all(name='h3', class_='title')
# print(movies)

top_100 = [i.getText() for i in movies][::-1]
# print(top_100)

with open('movies.txt', 'w', encoding='utf-8') as f:
    for i in top_100:
        f.write(i+'\n')
