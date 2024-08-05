# Web requests
import requests

# Export data
import json

# OS
import os

# Tracebacks
import traceback

# This query will contain the instructions of what we need from the AniList db
# including filters
query: str = '''
query ($page:Int) {
    Page (page:$page, perPage:50) {
        pageInfo {
            currentPage
            lastPage
            hasNextPage
        }
        media (type:ANIME, format:TV, status:FINISHED) {
            title{english romaji}
            countryOfOrigin
            source
            genres
            type
            format
            status
            episodes
            duration
            seasonYear
            season
            isLicensed
            popularity
            averageScore
            favourites
            studios (
            isMain:true
            ) {
                nodes{name}
            }
            relations {
                edges {
                    relationType(version:2)
                    node {
                        title{romaji english}
                        format
                        status
                        averageScore
                        popularity
                    }
                }
            }
        }
    }
}
'''

done: bool = False
page_num: int = 1
title_id: int = 1
data: dict = {}

# The following loop will go one page at a time through the database and,
# while doing so, it will extract the data from each page and store it in the
# 'data' variable, which we will finally export
while not done:
    print("Working with page #%d!" % page_num, end='\r')

    response: requests.Response = requests.post(
        "https://graphql.anilist.co", json={'query': query, 'variables':{"page":page_num}}
        )
    
    response_data: dict = response.json()

    try:

        if response_data['data']['Page']['pageInfo']['hasNextPage'] != True:
            done = True
        else:
            page_num +=1

    except TypeError:
        print(response.reason, response.json())
        traceback.print_exc()
        break

    titles: list[dict] = response_data['data']['Page']['media']

    for title in titles:
        data[title_id] = title

        title_id += 1

with open(os.path.join(
    os.path.dirname(__file__), 'data/titles_data.json'
    ), 'w') as json_file:
    json.dump(data, json_file, indent=4)
