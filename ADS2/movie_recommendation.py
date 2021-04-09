def count_discussability(friends: list, movies_dict: dict):
   '''
   fn: Method to count discussability of each movie

   :param friends: list, nested list with movies watched by friends
   :param movies_dict: dict, mapping from a movie string name to int
   :return: list, views count for each movie
   '''
   n = len(movies_dict)
   F_discuss = [0] * n

   for friend_movies in friends:
      for movie in movies_dict.keys():
         if movie in set(friend_movies):
            F_discuss[movies_dict[movie]] += 1

   return F_discuss

def edge2adj(edge_list: list, movies_dict: dict):
   '''
   fn: Method to convert edge list to adjacency list

   :param edge_list: list, list with similarities/edges of our graph
   :param movies_dict: dict, mapping from a movie string name to int
   :return: list, adjacency list of our graph
   '''
   adj = [[] for _ in range(len(movies_dict))]

   for edge in edge_list:
      adj[movies_dict[edge[0]]].append(movies_dict[edge[1]])
      adj[movies_dict[edge[1]]].append(movies_dict[edge[0]])
   
   return adj

def dfs(v: int, visited: list, discuss_count: int, F_discuss: list, graph: list):
   '''
   fn: DFS traversal method

   :param v: int, current vertice
   :param visited: list, list of visited vertices
   :param discuss_count: int, counter for the total value of friends who watched movies in the current component
   :param F_discuss: list, views count for each movie
   :param graph: list, adjacency list
   :return: list & int, list of visited vertices & discuss counter
   '''
   visited[v] = True

   # increase views value for the current component
   discuss_count += F_discuss[v]

   for u in graph[v]:
      if not visited[u]:
         visited, discuss_count = dfs(u, visited, discuss_count, F_discuss, graph)

   return visited, discuss_count

def find_count_components(adj_list: list, vertice: int, F_discuss: list, S_unique: dict):
   '''
   fn: Method for calculating uniqueness of each member of the component discovered by DFS

   :param adj_list: list, adjacency list
   :param vertice: int, vertice from which we start the DFS
   :param F_discuss: list, views count for each movie
   :param S_unique: dict, dictionary with uniqueness for each movie
   :return: dict, dictionary with uniqueness for each movie
   '''
   visited = [False] * len(adj_list)

   # counter for views as we traverse the graph
   discuss_count = 0
   
   visited, discuss_count = dfs(vertice, visited, discuss_count, F_discuss, adj_list)

   # length of component
   len_component = sum(visited)

   # corner case with only one vertice in component (i.e. movie doesn't have similar ones)
   if len_component == 1:
      # set uniqueness to zero as we'll skip those when calc'ing the final score
      S_unique[vertice] = 0
      return S_unique

   for i, was_visited in enumerate(visited):
      if was_visited:
         S_unique[i] = (discuss_count - F_discuss[i]) / (len_component - 1)

   return S_unique

def main(movies: list, similarities: list, friends: list):
   n = len(movies)

   movies_dict = dict(zip(movies, list(range(n))))
   
   # discussability
   
   F_discuss = count_discussability(friends, movies_dict)

   # similarities
   
   # convert from edge list to adjecncy list
   adj = edge2adj(similarities, movies_dict)
   
   # calculate uniqueness for each movie
   S_unique = {}
   for v in range(n):
      if v not in S_unique:
         S_unique = find_count_components(adj, v, F_discuss, S_unique)
   # calculate final score
   i_max, max_score = 0, 0

   for movie in range(n):
      if F_discuss[movie] != 0 and S_unique[movie] != 0:
         score = F_discuss[movie] / S_unique[movie]
         if score > max_score:
            max_score = score
            i_max = movie

   return movies[i_max]


if __name__ == '__main__':
   movies = ["Parasite", "1917", "Ford v Ferrari", "Jojo Rabbit", "Joker", "Twilight"]

   similarities = [["Parasite", "1917"],
                   ["Parasite", "Jojo Rabbit"],
                   ["Joker", "Ford v Ferrari"]]

   friends = [["Joker"],
               ["Joker", "1917"],
               ["Joker"],
               ["Parasite"],
               ["1917"],
               ["Jojo Rabbit", "Joker"]]

   print(main(movies, similarities, friends))
   
