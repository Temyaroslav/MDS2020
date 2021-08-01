## Project. Part 3

### Week 12.
<br><br>


Hello!

We are on a final week of our project and now it is time to scrape a little bit more data and write a report. This week you are expected to create a [word cloud](https://en.wikipedia.org/wiki/Tag_cloud) based on an actor's movies descriptions.

First of all, you are required to implement a function `get_movie_descriptions_by_actor_soup(actor_page_soup)`:

* This function takes a beautifulsoup soup object (`actor_page_soup`) of a page for the the current actor.
* The function should return a list strings. Each element is a short description of a movie, where the actor played. Every movie has such a description on its page.

Then we should get movie descriptions for every highest-paid actor of 2019. They are 

1. Dwayne Johnson
2. Chris Hemsworth
3. Robert Downey Jr.
4. Akshay Kumar
5. Jackie Chan
6. Bradley Cooper
7. Adam Sandler
8. Scarlett Johansson
9. Sofia Vergara
10. Chris Evans. 

Collect data and save it to files. Every actor should have a separate text file with descriptions of all movies an actor played in.

After that, for every actor you should provide a picture of a wordcloud, based on movie descriptions for that actor. To do so you might want to use [wordcloud python library](https://amueller.github.io/word_cloud/). Also, check out [this tutorial](https://www.datacamp.com/community/tutorials/wordcloud-python). Don't forget to get rid of stopwords.

As a result, you should have a jupyter notebook, where for every highest-paid actor of 2019 you read descriptions of all full feature fillms of that actor, then preprocess them (getting rid of stopwords), and then show a wordcloud based on these descriptions.

Checklist of this assignment:

* A function `get_movie_descriptions_by_actor_soup` is implemented
* Movie descriptions for every highest-paid actor of 2019 are collected and saved to files.
* Final report in jupyter notebook format contains a code, that for every actor reads movie descriptions, preprocess it (concatenation, getting rid of stopword) and prints out a wordcloud. So, we have 10 wordclouds overall.


This week you will be graded for all the work you had been working on for the last three weeks.

By the end of the week you should have

* `imdb_code.py` with all 4 functions implemented
* `imdb_helper_functions.py` with all helper functions that you used
* report in jupyter notebok format. Report contains an information about pairwise **movie distances** for the actors, network graphs (see week 11) and wordclouds based on movie discriptions.
* csv-file containing information about pairwise **movie distances**
* text files with movie description for every actor

Provide a ZIP-archive with these files.

<br><br><br>

### General summary for the review criteria.

* An archive contains files `imdb_code.py`, `imdb_helper_functions.py`, report in jupyter notebok format, csv-file containing information about pairwise **movie distances** and text files with movie description for every actor.

**Week 10 criteria** - **DONE**

* The functions implementation is present
* The functions somehow work, i.e. they return something for a given input
* The functions return format is correct (list of pairs)
* The functions have a possibility to limit the number of movies or actors in the output and it works.
* The function `get_movies_by_actor_soup` returns movies for both male and female actors
* The function `get_movies_by_actor_soup` returns movies where the current actor was involved as an actor, and not as somebody else (director, producer)
* The function get_movies_by_actor_soup returns only full feature films, and not something else (like TV series)
* The function `get_movies_by_actor_soup` returns only those films, that have been already released
* The function `get_actors_by_movie_soup` returns both male and female actors that played in the movie
* The function `get_actors_by_movie_soup` returns only actors (not some other crew members)

**Week 11 criteria** - **DONE**

* The functions implementation is present
* The function `get_movie_distance` somehow works, i.e. it returns something for a given input
* The function `get_movie_distance` works with URLs containing *www* and URLs not containing *www*
* The functions return format is correct (integer number)
* The functions `get_movie_distance` have a possibility to limit the number of movies or actors, i.e. arguments `num_of_actors_limit` and `num_of_movies_limit` could be passed and used inside the function

**Week 12 criteria - Network graphs** - **DONE**

* Final report has a code for plotting a network - **DONE**
* Final report has pictures of graphs - **DONE**
* Every node has a label (actor name) - **DONE**
* Every edge has a label (**movie distance** number, if it is less the infinity) - **DONE**
* Final report has pictures of graph of all pairwise **movie distances**. Edges for different **movie distances** are of different colours. For example, red colour for edges for **movie distances** equal to 1, green colour - for **movie distance** equal to 2, and so on. - **DONE**
* Final report has different pictures of graphs for different **movie distances**. There is a picture of a graph, where **movie distances** equal to 1 are visualised. Then there is a different picture, but where edges of **movie distances** equal to 2 only are visualised. And so on, for all different **movie distances** present. - **DONE**

**Week 12 criteria - wordcloud**

* A function `get_movie_descriptions_by_actor_soup` is implemented - **DONE**
* Movie descriptions for every highest-paid actor of 2019 are collected and saved to files. The files are present in the archive - **DONE**
* Final report contains a code for reading movie descriptions from files
* Final report contains a code for preprocess movie descriptions (concatenation, getting rid of stopword)
* Final report contains a code for printing out a wordcloud. 
* FInal report contains 10 wordclouds. One for each actor.