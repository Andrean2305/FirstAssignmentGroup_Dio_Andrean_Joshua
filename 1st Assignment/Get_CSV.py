from requests import get
from bs4 import BeautifulSoup
import pandas as panda

# Making CSV for stranger things series

# Fetching URL #
url = "https://www.imdb.com/title/tt4574334/episodes?season=" #stranger things
url2 = "https://www.imdb.com/title/tt3322312/episodes?season=" #dare devil
response = get(url)
print(response.text[:250])

# Parsing the content #
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

# Initalize List #
episodes = []

many_season_series1 = 4
many_season_series2 = 3

def get_series(website1,website2):
    for i in range (1,3):
        many = 0
        if (i == 1):
            many = 5
        elif(i == 2):
            many = 4
        for season in range(1, many):
            if (i == 1):
                response = get(
                    website1 + str(season))
            elif (i == 2):
                response = get(
                    website2 + str(season))

            # Parsing
            page_html = BeautifulSoup(response.text, 'html.parser')

            # Containers for episode
            episode_containers = page_html.find_all('div', class_='info')

            # Loop to compile the episode data
            #with this loop it will give you the range of season 1 - (5-1) why 5-1 because the program only read until it reach 5 and then it will break the loop
            for episodes in episode_containers:
                seasons = season
                episode_number = episodes.meta['content']
                title = episodes.a['title']
                airdate = episodes.find('div', class_='airdate').text.strip()
                rating = episodes.find('span', class_='ipl-rating-star__rating').text
                total_votes = episodes.find(
                    'span', class_='ipl-rating-star__total-votes').text
                desc = episodes.find('div', class_='item_description').text.strip()
                episode_data = [seasons, episode_number,
                                title, airdate, rating, total_votes, desc]

                # Appending the episode data into the data set

                episodes.append(episode_data)

# For all season in the Daredevil series #
get_series("https://www.imdb.com/title/tt4574334/episodes?season=","https://www.imdb.com/title/tt3322312/episodes?season=")
# Dataframe - Using Pandas #
episodes = panda.DataFrame(episodes, columns=[
    'season', 'episode_number', 'title', 'airdate', 'rating', 'total_votes', 'description'])
episodes.head()


# Conversion - Total Votes, Rating, AirDate to Numeric #


def remove_str(votes):
    for r in ((',', ''), ('(', ''), (')', '')):
        votes = votes.replace(*r)
    return votes

episodes['total_votes'] = episodes.total_votes.apply(
    remove_str).astype(int)

episodes.head()
episodes['rating'] = episodes.rating.astype(float)
episodes['airdate'] = panda.to_datetime(episodes.airdate)
episodes.info()

# Convert To CSV files
episodes.to_csv('DD_Stranger_Things_Episodes_IMDb_Ratings.csv', index=False)
