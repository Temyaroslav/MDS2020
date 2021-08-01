# define helper functions if needed
# and put them in `imdb_helper_functions` module.
# you can import them and use here like that:
import asyncio
import aiohttp
import numpy as np
import requests
import urllib
import re
from bs4 import BeautifulSoup

from imdb_helper_functions import *

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


async def get_async(name_urls: set, is_actor_soup: bool, num_of_movies_limit: int = None,
                    num_of_actors_limit: int = None):
    output = {}
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=2)) as session:
        for name_url in name_urls:
            url = name_url[1] if is_actor_soup else urllib.parse.urljoin(name_url[1], 'fullcredits/')
            print(name_url)
            async with session.get(url, ssl=False) as response:
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")
                try:
                    result = get_movies_by_actor_soup(soup,
                                                      num_of_movies_limit) if is_actor_soup else get_actors_by_movie_soup(
                        soup, num_of_actors_limit)
                    output[name_url[0]] = result
                except:
                    continue
    return output


def __check_distance(actor_end: tuple,
                     actors_to_check: list,
                     checked_actors: set,
                     checked_movies: set,
                     movies_cache: dict,
                     actors_cache: dict,
                     num_of_actors_limit: int = None,
                     num_of_movies_limit: int = None):
    # check for actors which are not in the cache yet
    missing_actors = set(filter(lambda x: x[0] not in actors_cache, actors_to_check))
    if len(missing_actors) != 0:
        print('Sending async get request for actors ..')
        actor_movies = asyncio.run(get_async(missing_actors, True, num_of_movies_limit, num_of_actors_limit))
        actors_cache.update(actor_movies)

    # get movies list from actor cache
    movies_to_check = []
    # (using filter here in case we could not cache some actors for some reasons (e.g. broken imdb page))
    for actor in filter(lambda x: x[0] in actors_cache, actors_to_check):
        movies_to_check += actors_cache[actor[0]]

    # check for movies cast which is not in the cache yet
    missing_movies = set(filter(lambda x: x[0] not in movies_cache, movies_to_check))
    if len(missing_movies) != 0:
        print('Sending async get request for movies cast ..')
        movies_cast = asyncio.run(get_async(missing_movies, False, num_of_movies_limit, num_of_actors_limit))
        movies_cache.update(movies_cast)

    # get adjacent actors using cached movies cast
    adjacent_actors = []
    for movie in filter(lambda x: x[0] not in checked_movies and x[0] in movies_cache, movies_to_check):
        adjacent_actors += movies_cache[movie[0]]
    # check if our end actor is among adjacent actors
    for actor in adjacent_actors:
        if actor[0] == actor_end[0]:
            return True, actors_to_check, checked_actors, checked_movies, movies_cache, actors_cache

    # save already checked actors and movies
    checked_actors = checked_actors.union(set(actors_to_check))
    checked_movies = checked_movies.union(set(movies_to_check))
    # leave only unchecked actors for the next iteration
    adjacent_actors = list(set(adjacent_actors) - checked_actors)

    return False, adjacent_actors, checked_actors, checked_movies, movies_cache, actors_cache


def __get_movie_path(actor_end, actor_path, movies_path, actors_cache, movies_cache):
    # recursive helper method to look for the paths in cache
    if len(actor_path) > 3:
        return

    parent_actor = actor_path[-1]
    for movie in actors_cache.get(parent_actor[0], []):
        if any(map(lambda x: x[0] == movie[0], movies_path)):
            continue
        for actor in movies_cache.get(movie[0], []):
            if any(map(lambda x: x[0] == actor[0], actor_path)):
                continue
            if actor[0] != actor_end[0]:
                __get_movie_path(actor_end, actor_path + [actor], movies_path + [movie], actors_cache, movies_cache)
            else:
                movies_path.append(movie)
                print(f'Found a {len(actor_path)} step path:')
                for x, y in zip(actor_path, movies_path):
                    print(x, '->', y, '->')
                print(actor_end)


def get_movie_path(actor_start: tuple, actor_end: tuple, actors_cache: dict = None, movies_cache: dict = None):
    # method used to print all the paths between cached actors
    if actors_cache is None or movies_cache is None:
        actors_cache, movies_cache = get_cache()

    assert actor_start[0] in actors_cache or actor_end[0] in actors_cache, 'Actors are not in the cache!'

    __get_movie_path(actor_end, [actor_start], [], actors_cache, movies_cache)


def get_movie_distance(actor_start_url: str, actor_end_url: str,
                       num_of_actors_limit: int = None, num_of_movies_limit: int = None,
                       print_path: bool = False) -> int:
    _headers = {'Accept-Language': 'en', 'X-FORWARDED-FOR': '2.21.184.0'}
    
    # get cached movies and actors data
    actors_cache, movies_cache = get_cache()

    # get start actor name
    response = requests.get(actor_start_url, headers=_headers)  # (should work with www and without)
    assert response.ok, 'Something wrong with the start actor!'
    soup = BeautifulSoup(response.text, "html.parser")
    actor_start = (extract_actor_name_from_soup(soup), actor_start_url)
    # get end actor name
    response = requests.get(actor_end_url, headers=_headers)
    assert response.ok, 'Something wrong with the end actor!'
    soup = BeautifulSoup(response.text, "html.parser")
    actor_end = (extract_actor_name_from_soup(soup), actor_end_url)

    actors_to_check, checked_actors, checked_movies = [actor_start], set(), set()

    current_distance = 1
    while current_distance <= 3:
        found, actors_to_check, \
        checked_actors, checked_movies, \
        movies_cache, actors_cache = __check_distance(actor_end, actors_to_check,
                                                      checked_actors, checked_movies,
                                                      movies_cache, actors_cache,
                                                      num_of_actors_limit, num_of_movies_limit)

        update_cache(actors_cache, movies_cache)

        if found:
            if print_path:
                get_movie_path(actor_start, actor_end, actors_cache, movies_cache)
            return current_distance

        current_distance += 1
    
    return np.inf


def get_movie_descriptions_by_actor_soup(actor_page_soup):
    # get actor name from the soup
    actor_name = extract_actor_name_from_soup(actor_page_soup)
    # get actor movies from the soup
    actor_movies = get_movies_by_actor_soup(actor_page_soup)
    descriptions = []
    for movie in actor_movies:
        print(movie)
        response = requests.get(movie[1])
        assert response.ok, f'Something wrong with {movie[0]} - {movie[1]}'
        soup = BeautifulSoup(response.text, 'html.parser')
        des = get_movie_description_from_soup(soup)
        descriptions.append(des)
    with open(f'{actor_name}.txt', 'w') as f:
        for des in descriptions:
            f.write(des + '\n')


if __name__ == '__main__':
    headers = {'Accept-Language': 'en', 'X-FORWARDED-FOR': '2.21.184.0'}
    highest_paid_actors = [
                            ('Dwayne Johnson', 'https://www.imdb.com/name/nm0425005/'),
                            ('Chris Hemsworth', 'https://www.imdb.com/name/nm1165110/'),
                            ('Robert Downey Jr.', 'https://www.imdb.com/name/nm0000375/'),
                            ('Akshay Kumar', 'https://www.imdb.com/name/nm0474774/'),
                            ('Jackie Chan', 'https://www.imdb.com/name/nm0000329/'),
                            ('Bradley Cooper', 'https://www.imdb.com/name/nm0177896/'),
                            ('Adam Sandler', 'https://www.imdb.com/name/nm0001191/'),
                            ('Scarlett Johansson', 'https://www.imdb.com/name/nm0424060/'),
                            ('Sofia Vergara', 'https://www.imdb.com/name/nm0005527/'),
                            ('Chris Evans', 'https://www.imdb.com/name/nm0262635/')
                            ]

    # UNIT TEST
    for url in highest_paid_actors:
        response = requests.get(url[1], headers=headers)
        assert response.ok
        soup = BeautifulSoup(response.text, 'html.parser')
        get_movie_descriptions_by_actor_soup(soup)

    # UNIT TEST

    # dist = get_movie_distance('https://www.imdb.com/name/nm0362766/', 'https://imdb.com/name/nm0000288/',
    # num_of_actors_limit=None, num_of_movies_limit=None, print_path=True)
    # print(f'Movie distance {dist}')

    # get_movie_path(('Dwayne Johnson', 'https://www.imdb.com/name/nm0425005/'), ('Jackie Chan', 'https://www.imdb.com/name/nm0000329/'))

    

    # import itertools

    # for perm in itertools.permutations(highest_paid_actors, 2):
    #     dist = get_movie_distance(perm[0][1], perm[1][1],
    #     num_of_actors_limit=5, num_of_movies_limit=5, print_path=True)
    #     print(f'Movie distance is {dist}')
