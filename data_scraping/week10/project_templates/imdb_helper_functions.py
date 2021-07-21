def check_correct_cast_el(el) -> bool:
    # check if an element in the cast table has the correct structure
    if 'class' in el.attrs:
        if el['class'][0] in {'odd', 'even'}:
            return len(el['class']) == 1
    
    return False

def check_uncredited(el) -> bool:
    # check if the actor is uncredited
    # if yes, we can break the loop earlier
    if '(uncredited)' in el.text:
        return True
    return False

def has_valid_parentheses(s) -> bool:
    # check if the string has balanced parentheses
    count = 0
    for i in s:
        if i == "(":
            count += 1
        elif i == ")":
            count -= 1
        if count < 0:
            return False
    return count == 0

def check_bad_movie_type(s) -> bool:
    # check if the movie string contains a bad movie type
    bad_types = ['TV Series', 'Short', 'Video Game', 'Video short', 'Video', 
    'TV Movie', 'TV Mini-Series', 'TV Series short', 'TV Mini Series', 'TV Special', 'Documentary short',
     'Documentary', 'voice', 'uncredited', 'unconfirmed']
    for bad_type in bad_types:
        if bad_type in s:
            return True
    return False

def check_bad_release(el) -> bool:
    # check if the movie was already released
    result = el.find_all('a')
    if len(result) != 1:
        return True
    return False

def extract_year(el) -> None:
    # remove the year from the movie element
    result = el.find('span', attrs={'class': 'year_column'})
    if len(result) != 0:
        result.extract()

def extract_movie_name_url(el):
    # extract movie name and url from the movie element
    result = el.find('b')
    result.extract()
    return result.text.strip(), result.find('a')['href']

def extract_actor_name_from_soup(actor_page_soup):
    name = actor_page_soup.find('span', attrs={'itemprop'}).text
    return name