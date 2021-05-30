## Project. Part 2

### Week 11.
<br><br>


Hello!

We continue working on our project. This week we want 

1. to implement a function, measuring *movie distance* between two actors
2. calculate *movie distances* between all highest-paid actors
3. visualise the distances as a graph

**Be aware, that collecting necessary data may take quite a time, so start in advance!**

**And before you start, please, read all the text below carefully.**

<br><br><br>

### 1. Measuring movie distance

Alright, we want to measure a *movie distance* between two actors. How can we do this? Here we will try to give you an idea and show you the reasoning. The following algorithm should be pretty straight-forward, but clearly not very efficient. If you want and if you have time, feel free to improve it as much as you can, and implement a more efficient version. But if you are struggling and do not know where to start, you can stay with this algorithm.

Let's clarify our goals. We want to define a function  `get_movie_distance(actor_start_url, actor_end_url,
        num_of_actors_limit=None, num_of_movies_limit=None)` from `imdb_code.py`.
        
* This function has two mandatory arguments: `actor_start_url`, `actor_end_url` - urls to imdb pages of actors, that we want to measure *movie distance* between
* This function should return an integer, a *movie distance* between the given actors
* The function may also get optional arguments `num_of_actors` and `num_of_movies`, but we will talk about them later.

So, how could we solve this problem? Let's look at the simple examples to get some intuition.

What if we try to find the *movie distance* between actors, who played in the same movie. How would we find the distance? We would collect all the movies, where actor_start played. Then, for every movie we would get a list of actors, who played in those movies. Let's call it `distance_level_1_list`, since this is a list of all actors, whose *movie distance* to actor_start is 1. Then, we would check the list for an `actor_end`. Does a list contain an actor? Since we are talking about actors who played in the same movie, an actor_end will be in that list. So, we found `actor_end`, and now we have an answer. The *movie distance* is 1 here.

But what if we are talking about actors, who did not play in the same movie? Let's say, we have actors, whose *movie distance* is two. Then `distance_1_list` would not contain an `actor_end`. We need to go deeper. And now we have to solve the original problem, but for every actor from `distance_1_list`. Since we are talking about actors, whose *movie distance* is two, we sooner or later will find an actor in `distance_level_1_list`, who played in the same movie with `actor_end`, and we will get an answer. The *movie distance* is 2 here.

So, the very straight-forward solution if the following:

1. Set `current_distance` = 1
2. Start with some actor. Get the list of movies for the actor. Get the list of actors for those movies.
3. Does a list contain an `actor_end`?
    1. If yes: 
        1. return `current_distance`
    2. If no: 
        1. Increase `current_distance` by 1
        2. repeat step 2 for all actors, whose *movie distance* to `actor_start` is equal to `current_distance-1`
4. To avoid an infinite loop, we might want to set a limit. For example, if `current_distance` is equal to 10, and we still have not find a connection between `actor_start` and `actor_end`, let's assume that there is no connection between them.

<br>

#### Problem complexity

The problem has an exponential complexity. What does it mean?

Let's assume, that an average actor plays in $N$ movies, and let's assume, that an average movie has $M$ actors.

If *movie distance* between two actors is one, then to find out this, our program on average would

1. get a list of all movies, where `actor_start` played - it means running `get_movies_by_actor_soup` function once.
* get a list of all actors, by running a function `get_actors_by_movie_soup` $M$ times (for every found movie)
* after that, it would check a list of $N \cdot M$ actors, to see, if `actor_end` is present.

But if a *movie distance* between two actors is equal to 2, then to find out this our program would need to go further. On average it would

1. get a list of all movies, where `actor_start` played - it means running `get_movies_by_actor_soup` function once.
* get a list of all actors, by running a function `get_movies_by_actor_soup` $M$ times
* after that, it would check a list of $N \cdot M$ actors, to see, if `actor_end` is present
* for every actor it should get a list of movies: so a function `get_movies_by_actor_soup` would have to be run $N \cdot M$ times. On average we will get $N^2 \cdot M$ movies
* Then for every movie we should get a list of actors. That is, running `get_actors_by_movie_soup` function $N^2 \cdot M$ times, and obtaining a list of $N^2 \cdot M^2$ actors on average

And so on. You see the logic. The larger the distance between actors, the more actors and movies we should check, the more URLs we need to get and parse. It means, that without optimizing your algorithm, the web-scraping process may take a lot of time.

If you are unable to improve the algorithm, then we suggest you to solve a less fun, but also a less time consuming variation of the project (more on this - in the next section). If you have enough time, enough programming experience or enough will, then we encourage you to come up with a more efficient algorithm and implement it.


<br>

#### How to improve algorithm


Let's point out some ideas, that may lead to a better efficiency, or other ways to improve your project and have more fun:

* You may encounter some actors and some movies several times. So, not to waste time on obtaining data, that you already asked for, it would be a good idea to keep track of information about actors and movies you've already encountered with. You could keep them in a special sets seen_movies and seen_actors. After you got new movies or new actors, you might want to filter out those, that have already been seen, and check only really new ones. And update those sets every time you observe a new item.
* You may want to implement some caching. Since sending HTTP-requests and getting HTTP-response is comparatively time consuming procedure (you realise it when you need to send several thousand requests), it would be a good idea to save some information locally. For example, you could keep the data about what actors played in the particular movie, or what movies this particular actor played in. When you will run your function `get_movie_distance` for the first time, it still would have to go and visit all the URLs. But after several runs, your function may have collected quite a history, so when you will run your function another time, for another input, a big chunk of the data could be get from your local storage, which would save you a lot of time. This caching may be implemented in many ways: you could create your own local database, or you just use simple Python dicts. Whatever works for you.
* You may want to add checkpoints, so you don't have to start from scratch, if your script stopped working by some reason (network connection problems, power outage or whatever else). You could do it as simple as that: once in a while, make your function save all your current status variables to a hard drive (`actors_start`, `actor_end`, `current_distance`, `distance_level_1_list` or whatever variables you would use). And if something breaks, you could specify that path to these files, and make function work from where it had stopped. Keep in mind though, that writing and reading from a hard drive is also comparatively time consuming procedure. So, you probably should not save your results after *every* little step.
* You may want to send HTTP-requests asynchronously. It is a confusing, but very powerful way. When python sends a request, it doesn't have to wait and do nothing, until response comes back. Python could go on and send other requests, while waiting for the first one to return with the message. Asynchronous programming may hugely improve speed performance of data scraping script. However, this is more of a topic of advanced software engineering, than basic data scraping. Those of you, who heard of it, or who are eager to learn (check previous week reading materials), are welcome to do so. But be reasonable in a number of requests per second.
* You might want to know not only a *movie distance* between actors (which, in the end, is just a number), but names of movies and actors that connect those input actors. If you are interested in that, feel free to implement such a function.

<br>

#### Some other advices:

* Test your functions before submitting! Make sure they work, come up with some different inputs and see, if your code works as expected.
* Don't forget about helper functions. A good way is to break bigger functions into smaller parts, and it is easier to test each part. Put your helper functions in `imdb_helper_functions.py`. Write as many helper functions, as you need.
* You might want to add some additional arguments and functionality to your functions. For example, a simple logging could be done as an additional function argument, that (when set to True) will allow us to see, what is going on inside a function by printing intermediate variable values. Logging helps us a lot in testing functions.
* Make sure your function works with URLs containing *www* and not containing, because both versions work on *imdb.com*

<br><br>

### 2. Calculate movies distances between all highest-paid actors

After step 1, we are going to have a function, that computes a *movie distance* between two actors. In this step we want you to use your code to obtain all pairwise move distances for highest-paid actors of 2019. They are
 
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

Collect data and save it to a file, we will need it soon.

Keep in mind, that the process of collecting data takes some time. More over, without improvements it is probably impossible to calculate the distances in a reasonable amount of time.

So, to simplify things a little, we suggest you to solve the problem with some limitations.

Remember those arguments `num_of_actors_limit` and `num_of_movies_limit` from functions `get_actors_by_movie_soup` and `get_movies_by_actor_soup`? That is where we are going to use them. We will set `num_of_movies_limit `equal to 5, and `num_of_actors_limit` equal to 5. 

Thus, we will be exploring not all the movies, where an actor played, but only 5 latest movies. And we will not look at all actors playing on a movie, but only those, who played top 5 roles.

More over, let's assume, that if a connection between two actors is bigger than 3, then there is no connection between the actors (infinite distance). 

Doing this will let you to obtain all needed data for all actors by several hours, without any algorithm improvements. But even simple improvements like filtering seen movies or seen actors, or caching will speed your code up.

Of course, after introducing such limitations we will not surely get a real *movie distance* between actors, but we will obtain an upper bound estimate. True *movie distance* should be less or equal to the one, that we get this way. That is still something.

Those of you, who want to get a real *movie distance*, please, go ahead and try. Improve your algorithm and get a real answer. Those, who will be struggling with improving, please, do a simpler version. There will be no punishment for that, because the difficulties require not advanced web-scraping skills, but rather advanced programming skills.

<br><br><br>

### 3. Visualising data

After completing two previous steps, we should have a dataset with *movie distances* between actors. Now the data need to be visualised. To do so, we need a python library for working with social networks. One of such libraries is [NetworkX](https://networkx.org/documentation/stable/), but you may use any other library you like.

What we want is to see a plot of network. So, we need

* To install a library for network analysis (NetworkX or any other)
* A picture of the graph of a network: nodes of a graph would be actors, edges would be their connections.
* Every node should have a label (actor name)
* Every edge should have a label (*movie distance* number, if it is less the infinity)
* Edges for different *movie distances* should be of different colours. For example, red colour for edges for *movie distances* equal to 1, green colour - for *movie distance* equal to 2, and so on.
* Additionally, we want a plot, where only edges for *movie distance* equal to 1 will be visualised. Then a different plot, but for edges for *movie distances* equal to 2. And so on.
* All plots should be presented in jupyter notebook.

There will be no instructions for how to do that, because that is a simple task and you have a link to the documentation. Exploring yet unknown libraries is a daily life of a web-scraper, so it would be a good practice. If you got a problem, don't forget to ask the Internet, other students or us on a forum.

Keep in mind, that to start visualising you don't have wait until you got all the needed data. You can start learning the library with artificial data, while your real data is being collected. And you can just substitute the appropriate numbers later.

Also, you don't need to submit these visualisations this week. We are going to check only get_movie_distance function this week, so if you are short out of time, make implementing that function your priority. Visualisation will be graded next week, but it is better to have it completed by the end of the current week, because there will be other problems to solve.

<br><br><br>

### General summary for the review criteria.


You are required to submit a ZIP-archive with two files

* `imdb_code.py`
* `imdb_helper_functions.py`

<br>
`imdb_code.py` should contain three functions implemented. The first two should had been implemented last week, so just add a code for a third one

* `get_actors_by_movie_soup`
* `get_movies_by_actor_soup`
* `get_movie_distance`

<br>
`imdb_helper_functions.py` should contain all helper functions necessary for your code to work.

We will check the following

* The functions implementation is present
* The function `get_movie_distance` somehow works, i.e. it returns something for a given input
* The function `get_movie_distance` works with URLs containing *www* and URLs not containing *www*
* The functions return format is correct (integer number)
* The functions `get_movie_distance` have a possibility to limit the number of movies or actors, i.e. arguments `num_of_actors_limit` and `num_of_movies_limit` could be passed and used inside the function