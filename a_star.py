__author__ = 'hakon0601'

import operator


class AStar():
    def __init__(self, search_method="Best-first"):
        self.open_nodes = []
        self.closed_nodes = []
        self.search_method = search_method

    def add_open(self, node):
        self.open_nodes.append(node)

    def add_closed(self, node):
        self.closed_nodes.append(node)

    def remove_open(self, node):
        self.open_nodes.remove(node)

    def remove_closed(self, node):
        self.closed_nodes.remove(node)

    def get_node_from_open(self):
        if self.search_method == "Best-first":
            return self.get_best_first_node()
        elif self.search_method == "Breadth-first":
            return self.get_breadth_first_node()
        elif self.search_method == "Depth-first":
            return self.get_depth_first_node()

    def get_best_first_node(self):
        return min(self.open_nodes, key=operator.attrgetter('f_value'))

    def get_breadth_first_node(self):
        #TODO
        raise NotImplementedError

    def get_depth_first_node(self):
        #TODO
        raise NotImplementedError


    def generic_algorithm(self, environment):
        self.add_open(environment.get_start_node())
        environment.get_start_node().set_g(0)
        environment.get_start_node().set_f(environment.get_start_node().g_value + environment.get_start_node().h_value)
        #Agenda loop while solution not found
        while self.open_nodes:
            node_x = self.get_node_from_open()
            if node_x.type == "G":
                break
            self.add_closed(node_x)
            self.remove_open(node_x)
            successor_nodes = environment.get_successor_nodes(node_x)
            for successor in successor_nodes:
                if successor in self.closed_nodes:
                    continue
                tentative_g = node_x.g_value + environment.dist_between(node_x, successor)
                if successor not in self.open_nodes or tentative_g < successor.g_value:
                    successor.set_parent(node_x)
                    successor.set_g(tentative_g)
                    successor.set_f(tentative_g + successor.h_value)
                    if successor not in self.open_nodes:
                        self.add_open(successor)
        return None if not self.open_nodes else node_x

    def do_first_step(self, environment):
        self.add_open(environment.get_start_node())
        environment.get_start_node().set_g(0)
        environment.get_start_node().set_f(environment.get_start_node().g_value + environment.get_start_node().h_value)

    def do_one_step(self, environment):
        if self.open_nodes:
            node_x = self.get_node_from_open()
            if node_x.type == "G":
                return node_x
            self.add_closed(node_x)
            self.remove_open(node_x)
            successor_nodes = environment.get_successor_nodes(node_x)
            for successor in successor_nodes:
                if successor in self.closed_nodes:
                    continue
                tentative_g = node_x.g_value + environment.dist_between(node_x, successor)
                if successor not in self.open_nodes or tentative_g < successor.g_value:
                    successor.set_parent(node_x)
                    successor.set_g(tentative_g)
                    successor.set_f(tentative_g + successor.h_value)
                    if successor not in self.open_nodes:
                        self.add_open(successor)
            return node_x
        else:
            return None