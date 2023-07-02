import pandas as pd
from algorithms import Node, DepthFirstSearch, BreadthFirstSearch


class Search:

    def __init__(self, library='small'):
        """
        Load data, based on given library:
        small = default directory (test files)
        large = proper directory
        """
        self.movies = pd.read_csv(f'{library}\movies.csv')
        self.people = pd.read_csv(f'{library}\people.csv')
        self.stars = pd.read_csv(f'{library}\stars.csv')
        self.start = None
        self.target = None
        self.path = None
        self.explored = set()
        self.num_explored = 0
        self.max_depth = 6

    def set_targets(self, source_name=None, target_name=None):
        """
        Finds ids of the given people
        """
        if len(self.people[self.people['name'] == source_name]):
            self.start = self.people[self.people['name'] == source_name]
        else:
            raise KeyError('First person not found')

        if len(self.people[self.people['name'] == target_name]):
            self.target = self.people[self.people['name'] == target_name]
        else:
            raise KeyError('Second person not found')

    def find_path(self, algorithm='BreadthFirstSearch'):
        """
        Returns the list of ([actor_id], [movie_id)
        that connect the source to the target.
        If no possible path, raise Exception.
        """
        if algorithm == 'BreadthFirstSearch':
            alg = BreadthFirstSearch()
        elif algorithm == 'DepthFirstSearch':
            alg = DepthFirstSearch()
        else:
            raise Exception('Algorithm not found')

        # searches for movies of given actor and add them to the search list
        starting_nodes = self.find_films_by_actor_id(self.start.id.iloc[0])
        for film in starting_nodes:
            node = Node(actor=self.start.id.iloc[0], film=film, parent=None)
            alg.add(node)

        # search based on given algorithm
        while True:
            if alg.empty():
                raise Exception('No solution')
            node = alg.remove()
            self.num_explored += 1
            if self.num_explored % 10 == 0:
                print(self.num_explored)
            if self.target.id.iloc[0] in self.find_actors_by_movie_id(node.film):
                actor = [self.target.id.iloc[0]]
                film = [node.film]
                flag = True
                while flag:
                    if node.parent is None:
                        flag = False
                    actor.append(node.actor)
                    film.append(node.film)
                    node = node.parent

                actor.reverse()
                film.reverse()
                self.path = (actor, film)
                return self.path

            # adds child nodes of the last node
            self.explored.add(node.film)
            for actor in self.find_actors_by_movie_id(node.film):
                for film in self.find_films_by_actor_id(actor):
                    if not alg.contains_state(film) and film not in self.explored:
                        child = Node(film=film, actor=actor, parent=node)
                        child.set_depth()
                        if child.depth > self.max_depth:
                            continue
                        alg.add(child)

    def show_path(self):
        """
        Prints path to the console
        """
        print(f'How to connect: {self.start.name.iloc[0]} and {self.target.name.iloc[0]} within 6 steps?\n')
        for i in range(len(self.path[0])-1):
            print(f'{self.find_actor_name_by_id(self.path[0][i])} and {self.find_actor_name_by_id(self.path[0][i+1])} '
                  f'played in {self.find_film_name_by_id(self.path[1][i])}')

    def find_films_by_actor_id(self, person_id):
        """ returns film of given actor based on his/her id """
        return self.stars[self.stars.person_id == person_id]['movie_id'].values

    def find_actors_by_movie_id(self, film_id):
        """ returns actors of given movie based on its id """
        return self.stars[self.stars.movie_id == film_id]['person_id'].values

    def find_actor_name_by_id(self, actor_id):
        """ returns actor full name based on his/her id"""
        return self.people[self.people.id == actor_id].name.iloc[0]

    def find_film_name_by_id(self, film_id):
        """ returns movie full name based on its id"""
        return self.movies[self.movies.id == film_id].title.iloc[0]
