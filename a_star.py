__author__ = 'hakon0601'

import operator


class AStar():
    def __init__(self, search_method):
        self.open_nodes = []
        self.closed_nodes = []
        self.search_method = search_method
        self.finished = False

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
            return self.find_best_first_node()
        elif self.search_method == "Breadth-first":
            return self.find_breadth_first_node()
        elif self.search_method == "Depth-first":
            return self.find_depth_first_node()

    def find_best_first_node(self):
        best_node = self.open_nodes[0]
        for node in self.open_nodes:
            if node.g_value + node.h_value < best_node.g_value + best_node.h_value:
                best_node = node
        return best_node
        #return min(self.open_nodes, key=operator.methodcaller('get_f'))

    def find_breadth_first_node(self):
        return self.open_nodes[0]
        # Alternatively
        # return min(self.open_nodes, key=operator.attrgetter('g_value'))

    def find_depth_first_node(self):
        return self.open_nodes[len(self.open_nodes) - 1]
        # Alternatively
        # return min(self.open_nodes, key=operator.attrgetter('h_value'))

    # Algorithm for solving in one step/loop
    def do_complete_algorithm(self, environment):
        self.add_open(environment.get_start_node())
        environment.get_start_node().g_value = 0
        #Agenda loop while solution not found
        while self.open_nodes:
            current_node = self.get_node_from_open()
            if current_node.type == "G":
                return current_node
            self.add_closed(current_node)
            self.remove_open(current_node)
            successor_nodes = environment.get_successor_nodes(current_node)
            for successor in successor_nodes:
                if successor in self.closed_nodes:
                    continue
                tentative_g = current_node.g_value + environment.movement_cost(current_node, successor)
                # If the cost of getting to successor node is better from going through current
                if successor not in self.open_nodes or tentative_g < successor.g_value:
                    successor.parent = current_node
                    successor.g_value = tentative_g
                    if successor not in self.open_nodes:
                        self.add_open(successor)
        return None

    def do_first_step(self, environment):
        self.add_open(environment.get_start_node())
        environment.get_start_node().g_value = 0

    # Go through algorithm incrementally
    def do_one_step(self, environment):
        if self.open_nodes:
            current_node = self.get_node_from_open()
            if current_node.type == "G":
                return environment.reconstruct_path(current_node)
            self.add_closed(current_node)
            self.remove_open(current_node)
            successor_nodes = environment.get_successor_nodes(current_node)
            for successor in successor_nodes:
                if successor in self.closed_nodes:
                    continue
                tentative_g = current_node.g_value + environment.movement_cost(current_node, successor)
                # If the cost of getting to successor node is better from going through current
                if successor not in self.open_nodes or tentative_g < successor.g_value:
                    successor.parent = current_node
                    successor.g_value = tentative_g
                    if successor not in self.open_nodes:
                        self.add_open(successor)
            # Means that the gui should continue calling the method
            return 1
        return None