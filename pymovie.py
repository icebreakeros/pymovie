from bs4 import BeautifulSoup
import pandas as pd
import lxml
import requests
import re


# Variables that we are going to use
i = 0
N = 25 # number of lines to print
place_lst = []
rating_lst = []
title_lst = []
year_lst = []
starring_lst = []

# Download IMDB's Top 250 data
url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')


movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

imdb = []

# Store each item into dictionary (data), then put those into a list (imdb)
for index in range(0, len(movies)):
        # Seperate movie into: 'place', 'title', 'year'
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    place = movie[:len(str(index))-(len(movie))]
    data = {"movie_title": movie_title,
            "year": year,
            "place": place,
            "star_cast": crew[index],
            "rating": ratings[index],
            "vote": votes[index],
            "link": links[index]}
    imdb.append(data)

'''
#Trying to use Pandas DataFrame
    test_df = pd.DataFrame({"movie_title": movie_title,
                            "rating": round(float(ratings[index]), 2),
                            "year": year,
                            "star_cast": crew[index],
                            "place": place})

print (test_df.info())
'''

for item in imdb:
    place_lst.append(item['place'])
    rating_lst.append(round(float(item['rating']), 1))
    title_lst.append(item['movie_title'])
    year_lst.append(item['year'])
    starring_lst.append(item['star_cast'])

for i in range(N):
    print (place_lst[i] + (4-len(place_lst[i]))*" " + str(rating_lst[i]) + (4-len(str(rating_lst[i])))*" " +\
           title_lst[i] + (50 - len(title_lst[i])) * " " + year_lst[i] + 4*" " +  starring_lst[i])

#    print(item['place'], '*', round(float(item['rating']), 2), '*', item['movie_title'], '('+item['year']+') *', 'Starring:', item['star_cast'])
