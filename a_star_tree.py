from a_star_general import AStarGeneral


class AStarTree(AStarGeneral):
    def __init__(self, search_method="Best-first"):
        AStarGeneral.__init__(self, search_method=search_method)

    # Go through algorithm incrementally
    def do_one_step(self):
        if self.open_nodes:
            current_node = self.get_node_from_open()
            #print "selected state: " + str(current_node)
            self.add_closed(current_node)
            # If the current node is the goal node
            if current_node.h_value == 0:
                return current_node
            # generate and get successor nodes
            successor_nodes = current_node.generate_successor_nodes()
            #print "successors: " + str(successor_nodes)
            for successor in successor_nodes:
                # No need for checking if a node has been generated.
                # This is a tree and nodes can only be generated from one parent
                self.attach_and_eval(successor, current_node)
                self.add_open(successor)
                current_node.children.append(successor)

            return current_node
        return None
