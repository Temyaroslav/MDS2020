# define helper functions if needed
# and put them in `imdb_helper_functions` module.
# you can import them and use here like that:
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
        if '(' in text and has_valid_parentheses(text):
            print('='*25)
            print(f'{movie_name} has some unidentified brackets:\n{text}')
        
        result.append((movie_name, urllib.parse.urljoin(_url, movie_url)))
    if num_of_movies_limit is None:
        return result
    else:
        return result[:num_of_movies_limit]


def get_movie_distance(actor_start_url, actor_end_url,
        num_of_actors_limit=None, num_of_movies_limit=None):
    # your code here
    return # your code here


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
    url = 'https://www.imdb.com/name/nm0272581/'
    # url = 'https://www.imdb.com/name/nm0000093/'
    # url = 'https://www.imdb.com/name/nm0000146/'
    # url = 'https://www.imdb.com/name/nm0000138/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    print(get_movies_by_actor_soup(soup))
