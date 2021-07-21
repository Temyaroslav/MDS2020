# define helper functions if needed
# and put them in `imdb_helper_functions` module.
# you can import them and use here like that:
import numpy as np
import pickle
import requests
import urllib
import re
from bs4 import BeautifulSoup
from imdb_helper_functions import *


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
        if '(' in text and has_valid_parentheses(text):
            print('='*25)
            print(f'{movie_name} has some unidentified brackets:\n{text}')
        
        result.append((movie_name, urllib.parse.urljoin(_url, movie_url)))
    if num_of_movies_limit is None:
        return result
    else:
        return result[:num_of_movies_limit]


def get_movie_distance(actor_start_url, actor_end_url,
        num_of_actors_limit=None, num_of_movies_limit=None) -> int:
    _headers = {'Accept-Language': 'en', 'X-FORWARDED-FOR': '2.21.184.0'}
    path = r'C:\\Users\\Yaroslav\\Documents\\MDS2020\\coding\\data_scraping\\week10\\project_templates\\'
    with open(path + 'movies_cache.pickle', 'rb') as f:
        movies_cache = pickle.load(f)
    with open(path + 'actors_cache.pickle', 'rb') as f:
        actors_cache = pickle.load(f)

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
    while current_distance <= 10:
        found, actors_to_check, checked_actors, movies_cache, actors_cache = __check_distance(actor_end, actors_to_check,
        checked_actors, movies_cache, actors_cache)
        
        with open(path + 'movies_cache.pickle', 'wb') as f:
            pickle.dump(movies_cache, f)
        with open(path + 'actors_cache.pickle', 'wb') as f:
            pickle.dump(actors_cache, f)

        if found:
            return current_distance

        current_distance += 1
    
    return np.inf


def get_movie_descriptions_by_actor_soup(actor_page_soup):
    # your code here
    return # your code here


if __name__ == '__main__':
    headers = {'Accept-Language': 'en', 'X-FORWARDED-FOR': '2.21.184.0'}

    # STRESS TEST

    # import pickle
    # path = r'C:\\Users\\Yaroslav\\Documents\\MDS2020\\coding\\data_scraping\\week10\\all_movies_links'
    # with open(path, 'rb') as f:
    #     all_movies_links = pickle.load(f)
    # for name, name_url in all_movies_links.items():
    #     url = urllib.parse.urljoin(name_url, 'fullcredits/')
    #     response = requests.get(url, headers=headers)
    #     assert response.ok, f'Something wrong with the {name} url!'
    #     soup = BeautifulSoup(response.text, features="html.parser")
    #     print(name, '---->', get_actors_by_movie_soup(soup, 3))
    #     break

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

    # UNIT TEST
    
    dist = get_movie_distance('https://www.imdb.com/name/nm0000138/', 'https://www.imdb.com/name/nm0331516/')
    print(f'Movie distance is {dist}')
