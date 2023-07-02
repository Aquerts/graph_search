class Node:

    def __init__(self, actor, film, parent):
        self.actor = actor
        self.film = film
        self.parent = parent
        self.depth = 0

    def set_depth(self):
        if self.parent is not None:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 1


class DepthFirstSearch:

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, film):
        return any(node.film == film for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception('Empty frontier')
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class BreadthFirstSearch(DepthFirstSearch):

    def remove(self):
        if self.empty():
            raise Exception('Empty frontier')
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
