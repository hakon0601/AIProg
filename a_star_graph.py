from collections import defaultdict
from a_star_general import AStarGeneral


class AStarGraph(AStarGeneral):
    def __init__(self, search_method="Best-first"):
        AStarGeneral.__init__(self, search_method=search_method)
        self.generated_states = defaultdict(lambda: None)

    # Update all g values and parents along a new improved path
    def propagate_path_improvement(self, successor):
        for child_state in successor.children:
            tentative_g = successor.g_value + successor.movement_cost(child_state)
            if tentative_g < child_state.g_value:
                child_state.parent = successor
                child_state.g_value = tentative_g
                self.propagate_path_improvement(child_state)

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
                # If the successor is already generated use that instance instead
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
