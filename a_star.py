import operator
from heapq import heappush, heappop, heapify

class AStar():
    def __init__(self, search_method="Best-first"):
        self.open_nodes = []
        if search_method == "Best-first": heapify(self.open_nodes)
        self.closed_nodes = []
        self.search_method = search_method
        self.finished = False

    def add_open(self, node):
        if self.search_method == "Best-first":
            heappush(self.open_nodes, node)
        else:
            self.open_nodes.append(node)

    def add_closed(self, node):
        self.closed_nodes.append(node)

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

    def propagate(self, successor, g_value):
        successor.g_value = g_value
        if self.search_method == "Best-first":
            self.open_nodes.sort()

    # Go through algorithm incrementally
    def do_one_step(self):
        if self.open_nodes:
            current_node = self.get_node_from_open()
            print "current_node: " + str(current_node)
            # If the current node is the goal node
            if current_node.h_value == 0:
                print "Done"
                return current_node.reconstruct_path()
            self.add_closed(current_node)
            # generate and get successor nodes
            successor_nodes = current_node.generate_successor_nodes()
            for successor in successor_nodes:
                # if successor is closed, it is not relevant anymore
                if successor in self.closed_nodes:
                    continue
                # calculates successors g_value with the new parent
                tentative_g = current_node.g_value + current_node.movement_cost(successor)
                # append parent to successor
                successor.parents.append(current_node)
                if successor in self.open_nodes:
                    # updates successors g_value if it is better
                    if tentative_g < successor.g_value:
                        self.propagate(successor, tentative_g)
                else:
                    #if self.search_method == "Best-first":
                        #print("order: " + str(successor))
                    # place successor in open node and set g_value (it is not yet explored)
                    successor.g_value = tentative_g
                    self.add_open(successor)

            # Means that the gui should continue calling the method
            return 1
        return None