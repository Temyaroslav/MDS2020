## Project. Part 1

### Week 10.

<br><br>

Hello!

We are starting to work on the final project, where we are going to collect, process, analyse and present data from imdb.com. The project is split into three parts to help you work consistently. The final submission (which costs about 21% of the final grade) is expected on the week 12. On weeks 11 & 12 you are expected to submit intermediate results (they cost 2% of the final grade each). Going through the project step by step and submitting intermediate results will increase the chance of successful final submission, because you will be able to get intermediate feedback (and thus fix your projects before the final submission). Also, It is always easier tackling several small problems, than tackling the only problem, but a big one. And remember: you can not pass a course without passing the final project. So, we encourage you to devote your time to working on the project during all three weeks. Do not leave all the work for the final week, because you might risk not passing the course. So, plan your time accordingly.

Have you heard of [Six degrees of separation](https://en.wikipedia.org/wiki/Six_degrees_of_separation) theory? Have you heard of the game [Six Degrees of Kevin Bacon](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon)? Well, our first goal in the project will be to implement a function, that will help us play this game.

The idea is simple. We introduce a special measure of distance between actors. How is it measured? If two actors played in the same movie, the distance between them is 1. If two actors never played in the same move, but there is some actor, who played in some movies with each of the actors, then the distance between the actors is 2. And so on. You can play around [here](https://oracleofbacon.org/help.php) to get a feel. Let's call it *movie distance*.

During first two weeks of the project, we will be implementing a function, counting a distance between given actors. We will be using data from [IMDB](https://imdb.com) to obtain such an information. Then, we will try to visualize this data.

<br><br><br>

### Detailed description

This task is not so easy, so we will solve the problem step by step. This week you are required to implement two auxiliary functions, that will be used for obtaining data the following week. Two functions are required:

* we want to be able to get a list of movies that a current actor played in
* we want to be able to get a list of actors, that played in the current movie

Get [this](https://github.com/magnitofonov/hse-coursera-data-scraping/tree/master/week10/project_templates) code template. This week, implement functions `get_actors_by_movie_soup` and `get_movies_by_actor_soup`. There are some other functions templates also, but leave them as they are for a while. We will implement them in the following weeks. Let's talk more precisely, what these functions are about and how they should behave:

`get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit)`

* This function takes a beautifulsoup soup object (`cast_page_soup`) of a page for the cast & crew for the current film.
* The function should return a list of all actors that played in the movie. An actor should be defined by such a pair: `(name_of_actor, url_to_actor_page)`. So, the output of the function is expected to be the list of such pairs.
* The function should be able to take an optional argument `num_of_actors`. This argument allows us to limit the output. If we set the argument equal to, say, 10, then the function should return first 10 actors listed on the cast page, and no more than that. If we set the argument equal to `None`, then the function should return all the actors.

`get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit)`

* This functions takes a beautifulsoup soup object (`actor_page_soup`) of a page for the current actor.
* The function should return a list of all movies that the actor played in. A movie should be defined by such a pair: `(name_of_movie, url_to_movie_page)`. So, the output of the function is expected to be the list of such pairs.
* The function should be able to take an optional argument `num_of_movies_limit`. This argument allows us to limit the output. If we set the argument equal to, say, 10, then the function should return 10 latest movies that the actor played in, and no more than that. If we set the argument equal to None, then the function should return all the movies.
* The function should return only those movies, that have already been released.
* Sometimes actors could be producers, or even directors, or something else. The function should return only those movies, where the actor did an acting job. So, we should omit all the movies, where the actor has not actually played a role.
* The function should return only full feature movies. So, it should omit other types of videos, which are marked on imdb like that: TV Series, Short, Video Game, Video short, Video, TV Movie, TV Mini-Series, TV Series short and TV Special.


You may want to define supplementary functions, to make your code better. So, feel free to implement any additional functions you might need, but place them in [`imdb_helper_functions.py`](https://github.com/magnitofonov/hse-coursera-data-scraping/tree/master/week10/project_templates) file (we want to keep additional functions separated from essential function, so it would be easier to check your code). You can import these functions to your `imdb_code.py` script or to jupyter notebook, and use them there.

Also, when you are done with the functions, think about the following actions. Next week we will be implementing a function, that takes two actors as an input, and returns the *movie distance* between actors. Try to come up with an algorithm, that would solve such a problem.

<br>

#### Some advices:

* Test your functions before submitting! Make sure they work, try out different input. Answer the following questions: does your function return movies for both male and female actors? Does your function return movies where the current actor was involved as an actor, and not as somebody else (director, producer)? Does your function return only full feature films, and not something else (like TV series)? Does your function return only those films, that have been already released?
* Don't forget about helper functions. A good way is to break bigger functions into smaller parts, and it is easier to test each part. Put your helper functions in `imdb_helper_functions.py`.
* You might want to add some additional arguments and functionality to your functions. For example, a simple logging could be done as an additional function argument, that (when set to `True`) will allow us to see, what is going on inside a function by printing intermediate variable values. Logging helps us a lot in testing functions.

<br><br><br>

### General summary for the review criteria.

You are required to submit a ZIP-archive with two files

* `imdb_code.py`
* `imdb_helper_functions.py`

`imdb_code.py` should contain two functions implemented

* `get_actors_by_movie_soup`
* `get_movies_by_actor_soup`

`imdb_helper_functions.py` should contain all helper functions necessary for your code to work.

**We will check the following**

* The functions implementation is present
* The functions somehow work, i.e. they return something for a given input
* The functions return format is correct (list of pairs)
* The functions have a possibility to limit the number of movies or actors in the output and it works.
* The function `get_movies_by_actor_soup` returns movies for both male and female actors
* The function `get_movies_by_actor_soup` returns movies where the current actor was involved as an actor, and not as somebody else (director, producer)
* The function `get_movies_by_actor_soup` returns only full feature films, and not something else (like TV series)
* The function `get_movies_by_actor_soup` returns only those films, that have been already released
* The function `get_actors_by_movie_soup` returns both male and female actors that played in the movie
* The function`get_actors_by_movie_soup` returns only actors (not some other crew members)