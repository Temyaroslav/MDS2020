# define helper functions if needed
# and put them in `imdb_helper_functions` module.
# you can import them and use here like that:
import asyncio
import aiohttp
import numpy as np
import pickle
import requests
import urllib
import re
from bs4 import BeautifulSoup
from imdb_helper_functions import *

async def get_async(name_urls: set, is_actor_soup: bool, num_of_movies_limit: int = None, num_of_actors_limit: int = None):
    output = {}
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=2)) as session:
        for name_url in name_urls:
            url = name_url[1] if is_actor_soup else urllib.parse.urljoin(name_url[1], 'fullcredits/')
            print(name_url)
            async with session.get(url, ssl=False) as response:
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")
                try:
                    result = get_movies_by_actor_soup(soup, num_of_movies_limit) if is_actor_soup else get_actors_by_movie_soup(soup, num_of_actors_limit)
                    output[name_url[0]] = result
                except:
                    continue
    return output

def __check_distance(actor_end: tuple, actors_to_check: list, checked_actors: set, movies_cache: dict, actors_cache: dict,
                num_of_actors_limit: int = None, num_of_movies_limit: int = None):
    movies_to_check, adjacent_actors = [], []

    for actor in actors_to_check:
        print('Checking actor: ', actor)
        if actor[0] in actors_cache:
            print('Cached.')
            movies_to_check += actors_cache[actor[0]]
        else:
            print('Sending http request.')
            response = requests.get(actor[1], headers={'Accept-Language': 'en', 'X-FORWARDED-FOR': '2.21.184.0'})
            assert response.ok
            actor_page_soup = BeautifulSoup(response.text, "html.parser")
            movies = get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit)
            movies_to_check += movies
            actors_cache[actor[0]] = movies

        for movie in movies_to_check:
            print('Checking movie: ', movie)
            if movie[0] in movies_cache:
                print('Cached.')
                adjacent_actors += movies_cache[movie[0]]
            else:
                print('Sending http request.')
                response = requests.get(urllib.parse.urljoin(movie[1], 'fullcredits/'),
                headers={'Accept-Language': 'en', 'X-FORWARDED-FOR': '2.21.184.0'})
                assert response.ok
                movie_cast_soup = BeautifulSoup(response.text, "html.parser")
                actors = get_actors_by_movie_soup(movie_cast_soup, num_of_actors_limit)
                adjacent_actors += actors
                movies_cache[movie[0]] = actors
    
    for actor in adjacent_actors:
        if actor[0] == actor_end[0]:
            return True, actors_to_check, checked_actors, movies_cache, actors_cache
    
    checked_actors = checked_actors.union(set(actors_to_check))
    adjacent_actors = list(set(adjacent_actors) - checked_actors)
    return False, adjacent_actors, checked_actors, movies_cache, actors_cache

def __check_distance2(actor_end: tuple, actors_to_check: list, checked_actors: set, movies_cache: dict, actors_cache: dict,
                num_of_actors_limit: int = None, num_of_movies_limit: int = None):
    # check for actors which are not in the cache yet
    # TODO: use set to get unique missing actors
    missing_actors = set(filter(lambda x: x[0] not in actors_cache, actors_to_check))
    if len(missing_actors) != 0:
        print('Sending async get request for actors ..')
        actor_movies = asyncio.run(get_async(missing_actors, True, num_of_movies_limit, num_of_actors_limit))
        actors_cache.update(actor_movies)
    
    # get movies list from actor cache
    movies_to_check = []
    for actor in filter(lambda x: x[0] in actors_cache, actors_to_check):
        movies_to_check += actors_cache[actor[0]]
    
    # check for movies cast which is not in the cache yet
    # TODO: use set to get unique missing movies
    missing_movies = set(filter(lambda x: x[0] not in movies_cache, movies_to_check))
    if len(missing_movies) != 0:
        print('Sending async get request for movies cast ..')
        movies_cast = asyncio.run(get_async(missing_movies, False, num_of_movies_limit, num_of_actors_limit))
        movies_cache.update(movies_cast)

    # get adjacent actors using cached movies cast
    adjacent_actors = []
    for movie in movies_to_check:
        adjacent_actors += movies_cache[movie[0]]
    # check if our end actor is among adjacent actors
    for actor in adjacent_actors:
        if actor[0] == actor_end[0]:
            return True, actors_to_check, checked_actors, movies_cache, actors_cache
    
    checked_actors = checked_actors.union(set(actors_to_check))
    adjacent_actors = list(set(adjacent_actors) - checked_actors)
    return False, adjacent_actors, checked_actors, movies_cache, actors_cache

def get_actors_by_movie_soup(cast_page_soup: BeautifulSoup, num_of_actors_limit: int = None) -> list:
    
    _url = 'https://www.imdb.com/'
    result = []
    # find table with the cast
    soup = cast_page_soup.find_all('table', attrs={'class': 'cast_list'})
    # find records in the table
    soup = soup[0].find_all('tr')
    # iterate over the records
    for el in soup:
        if not check_correct_cast_el(el):
            continue
        # decided not to include uncredited actors as well
        if check_uncredited(el):
            break

        name = el.find_all('a')[1]
        result.append((name.text.strip(), urllib.parse.urljoin(_url, name['href'])))
        
    if num_of_actors_limit is None:
        return result
    else:
        return result[:num_of_actors_limit]


def get_movies_by_actor_soup(actor_page_soup: BeautifulSoup, num_of_movies_limit: int = None) -> list:
    _url = 'https://www.imdb.com/'
    result = []
    soup = actor_page_soup.find_all('div', attrs={'id': re.compile('actor-*'), 'class': 'filmo-row'})
    # check if it is actor or actress
    if len(soup) == 0:
        soup = actor_page_soup.find_all('div', attrs={'id': re.compile('actress-*'), 'class': 'filmo-row'})
    assert len(soup) != 0, 'Something wrong with the actor/actress soup.'
    for el in soup:
        # get rid of year
        extract_year(el)

        # check for the release and movie type
        if check_bad_release(el) or check_bad_movie_type(el.text.strip()):
            continue

        # get movie name and url
        movie_name, movie_url = extract_movie_name_url(el)
        # get element text
        text = el.text.strip()

        # check if there are some unidentified brackets left
        # if '(' in text and has_valid_parentheses(text):
        #     print('='*25)
        #     print(f'{movie_name} has some unidentified brackets:\n{text}')
        
        result.append((movie_name, urllib.parse.urljoin(_url, movie_url)))
    if num_of_movies_limit is None:
        return result
    else:
        return result[:num_of_movies_limit]


def get_movie_distance(actor_start_url, actor_end_url,
        num_of_actors_limit=None, num_of_movies_limit=None) -> int:
    _headers = {'Accept-Language': 'en', 'X-FORWARDED-FOR': '2.21.184.0'}
    # path = r'C:\\Users\\Yaroslav\\Documents\\MDS2020\\coding\\data_scraping\\week10\\project_templates\\'
    path = '/Users/ytemchuk/Documents/MDS2020/data_scraping/week10/project_templates/'
    # get cached movies and actors data
    # with open(path + 'movies_cache.pickle', 'rb') as f:
    #     movies_cache = pickle.load(f)
    # with open(path + 'actors_cache.pickle', 'rb') as f:
    #     actors_cache = pickle.load(f)

    actors_cache, movies_cache = get_cache()

    response = requests.get(actor_start_url, headers=_headers)
    assert response.ok
    soup = BeautifulSoup(response.text, "html.parser")
    actor_start =  (extract_actor_name_from_soup(soup), actor_start_url)

    response = requests.get(actor_end_url, headers=_headers)
    assert response.ok
    soup = BeautifulSoup(response.text, "html.parser")
    actor_end =  (extract_actor_name_from_soup(soup), actor_end_url)

    actors_to_check, checked_actors = [actor_start], set()

    current_distance = 1
    while current_distance <= 3:
        found, actors_to_check, checked_actors, movies_cache, actors_cache = __check_distance2(actor_end, actors_to_check,
        checked_actors, movies_cache, actors_cache, num_of_actors_limit, num_of_movies_limit)
        
        with open(path + 'movies_cache.pickle', 'wb') as f:
            pickle.dump(movies_cache, f)
        with open(path + 'actors_cache.pickle', 'wb') as f:
            pickle.dump(actors_cache, f)
        # update_cache(actors_cache, movies_cache)

        if found:
            return current_distance

        current_distance += 1
    
    return np.inf


def get_movie_descriptions_by_actor_soup(actor_page_soup):
    # your code here
    return # your code here


if __name__ == '__main__':
    headers = {'Accept-Language': 'en', 'X-FORWARDED-FOR': '2.21.184.0'}

    # UNIT TEST

    # dist = get_movie_distance('https://www.imdb.com/name/nm0001191/', 'https://imdb.com/name/nm0262635/',
    # num_of_actors_limit=5, num_of_movies_limit=5)
    # print(f'Movie distance is {dist}')

    highest_paid_actors = [
                            # ('Dwayne Johnson', 'https://www.imdb.com/name/nm0425005/'),
                            # ('Chris Hemsworth', 'https://www.imdb.com/name/nm1165110/'),
                            # ('Robert Downey Jr.', 'https://www.imdb.com/name/nm0000375/'),
                            ('Akshay Kumar', 'https://www.imdb.com/name/nm0474774/'),
                            # ('Jackie Chan', 'https://www.imdb.com/name/nm0000329/'),
                            # ('Bradley Cooper', 'https://www.imdb.com/name/nm0177896/'),
                            # ('Adam Sandler', 'https://www.imdb.com/name/nm0001191/'), 
                            # ('Scarlett Johansson', 'https://www.imdb.com/name/nm0424060/'),
                            ('Sofia Vergara', 'https://www.imdb.com/name/nm0005527/'),
                            # ('Chris Evans', 'https://www.imdb.com/name/nm0262635/')
                            ]
    
    import itertools

    for perm in itertools.permutations(highest_paid_actors, 2):
        dist = get_movie_distance(perm[0][1], perm[1][1],
        num_of_actors_limit=5, num_of_movies_limit=5)
        print(f'Movie distance is {dist}')

    # UNIT TEST
    
    # url = 'https://www.imdb.com/title/tt1160419/fullcredits/'
    # url = 'https://www.imdb.com/title/tt7131622/fullcredits/'
    # url = 'https://www.imdb.com/title/tt0109830/fullcredits/'
    # response = requests.get(url, headers=headers)
    # soup = BeautifulSoup(response.text, features="html.parser")
    # print(get_actors_by_movie_soup(soup))

    # UNIT TEST
    # url = 'https://www.imdb.com/name/nm0397171/'
    # url = 'https://www.imdb.com/name/nm0272581/'
    # url = 'https://www.imdb.com/name/nm0000093/'
    # url = 'https://www.imdb.com/name/nm0331516/'
    # url = 'https://www.imdb.com/name/nm0000138/'
    # response = requests.get(url, headers=headers)
    # soup = BeautifulSoup(response.text, features="html.parser")
    # print(get_movies_by_actor_soup(soup))