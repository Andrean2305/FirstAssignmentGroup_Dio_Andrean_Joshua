from requests import get
from bs4 import BeautifulSoup
import pandas as panda

# Making CSV for stranger things series

# Fetching URL #
url = "https://www.imdb.com/title/tt4574334/episodes?season=" #stranger things
url2 = "https://www.imdb.com/title/tt3322312/episodes?season=" #dare devil

url_cast1 = "https://www.imdb.com/title/tt4593118/?ref_=ttep_ep"
response = get(url)
print(response.text[:250])

# Parsing the content #
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

# Initalize List #
all_episodes = []
print ("How many series you want to compare: ")
input_many_website = int(input())

all_website = []
many_season = []
for i in range (1,input_many_website + 1) :
    print(f"Number {i} website code: ")
    input_website_now = input()
    all_website.append("https://www.imdb.com/title/" + input_website_now + "/episodes?season=")

    print (f"How many season in that series: ")
    input_series_now = int(input())
    many_season.append(input_series_now)

def get_series(many_website):
    for i in range (1,many_website + 1):
        many = many_season[i - 1]
        for season in range(1, many + 1):
            website = all_website[i - 1]
            response = get(website + str(season))

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

                all_episodes.append(episode_data)


# For all season in the Daredevil series #

get_series(input_many_website)
# Dataframe - Using Pandas #
all_episodes = panda.DataFrame(all_episodes, columns=[
    'season', 'episode_number', 'title', 'airdate', 'rating', 'total_votes', 'description'])
all_episodes.head()


# Conversion - Total Votes, Rating, AirDate to Numeric #


def remove_str(votes):
    for r in ((',', ''), ('(', ''), (')', '')):
        votes = votes.replace(*r)
    return votes

all_episodes['total_votes'] = all_episodes.total_votes.apply(
    remove_str).astype(int)

all_episodes.head()
all_episodes['rating'] = all_episodes.rating.astype(float)
all_episodes['airdate'] = panda.to_datetime(all_episodes.airdate)
all_episodes.info()

# Convert To CSV files
all_episodes.to_csv('DDD_Stranger_Things_Episodes_IMDb_Ratings.csv', index=False)
