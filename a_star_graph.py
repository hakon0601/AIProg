from heapq import heappush, heappop, heapify
from collections import defaultdict


class AStar_graph():
    def __init__(self, search_method="Best-first"):
        self.open_nodes = []
        if search_method == "Best-first": heapify(self.open_nodes)
        self.closed_nodes = set()
        self.generated_states = defaultdict(lambda: None)
        self.search_method = search_method
        self.finished = False

    def add_open(self, node):
        if self.search_method == "Best-first":
            heappush(self.open_nodes, node)
        else:
            self.open_nodes.append(node)

    def add_closed(self, node):
        self.closed_nodes.add(node)

    def get_node_from_open(self):
        if self.search_method == "Best-first":
            return self.find_best_first_node()
        elif self.search_method == "Breadth-first":
            return self.find_breadth_first_node()
        elif self.search_method == "Depth-first":
            return self.find_depth_first_node()

    def find_best_first_node(self):
        # Returns the open node with the lowest f value. If two have the same f, order by h
        return heappop(self.open_nodes)

    def find_breadth_first_node(self):
        # First-in-first-out
        return self.open_nodes.pop(0)

    def find_depth_first_node(self):
        # Last-in-first-out
        return self.open_nodes.pop(-1)

    def add_start_state_to_open(self, start_state):
        self.add_open(start_state)
        start_state.g_value = 0
        start_state.h_value = start_state.calculate_h()
        self.generated_states[start_state.getID()] = start_state

    # Update all g values and parents along a new improved path
    def propagate_path_improvement(self, successor):
        for child_state in successor.children:
            tentative_g = successor.g_value + successor.movement_cost(child_state)
            if tentative_g < child_state.g_value:
                child_state.parent = successor
                child_state.g_value = tentative_g
                self.propagate_path_improvement(child_state)

    def attach_and_eval(self, successor, current_node):
        successor.parent = current_node
        successor.g_value = current_node.g_value + current_node.movement_cost(successor)
        successor.h_value = successor.calculate_h()

    # Go through algorithm incrementally
    def do_one_step(self):
        if self.open_nodes:
            current_node = self.get_node_from_open()
            print "selected state: " + str(current_node)
            self.add_closed(current_node)
            # If the current node is the goal node
            if current_node.h_value == 0:
                return current_node
            # generate and get successor nodes
            successor_nodes = current_node.generate_successor_nodes()
            print "successors: " + str(successor_nodes)
            for successor in successor_nodes:
                # If the successor is already generated
                if self.generated_states[successor.getID()]:
                    successor = self.generated_states[successor.getID()]

                    tentative_g = current_node.g_value + current_node.movement_cost(successor)
                    if tentative_g < successor.g_value:
                        self.attach_and_eval(successor, current_node)
                        if successor in self.closed_nodes:
                            self.propagate_path_improvement(successor)
                        # We have to resort our heap when we internally change a value the heap is sorted on.
                        if self.search_method == "Best-first":
                            self.open_nodes.sort()
                else:
                    # Successor is not generated
                    # Defaultdict will create new item (instead of error) since key is not there
                    self.generated_states[successor.getID()] = successor
                    self.attach_and_eval(successor, current_node)
                    self.add_open(successor)

                current_node.children.append(successor)

            return current_node
        return None