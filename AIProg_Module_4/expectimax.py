
class Expectimax():
    # returns terminal value, return the best value for max, best value for minimax
    def __init__(self):
        return

    def run_expectimax(self, node, depth, a, b, chance):
        if depth == 0:
            node.set_h()
            return node.h_value

        if chance==None:
            r = node.generate_max_successor_nodes()
            if len(r) == 0 or r == None:
                return None
            left = right = up = down = None
            for child in node.children:
                if child.move == "left":
                    left = max(a, self.run_expectimax(child, depth-1, a, b, True))
                elif child.move == "right":
                    right = max(a, self.run_expectimax(child, depth-1, a, b, True))
                elif child.move == "up":
                    up = max(a, self.run_expectimax(child, depth-1, a, b, True))
                elif child.move == "down":
                    down = max(a, self.run_expectimax(child, depth-1, a, b, True))
            result =  max(left,right,up,down)
            #Returns which move to make
            if result==left:
                return "left"
            elif result==right:
                return "right"
            elif result==up:
                return "up"
            elif result==down:
                return "down"

        # Chance function
        elif chance:
            # this is a left, right, up, down node
            # generate successors and returns the average value
            # a = -inf, b = inf
            node.generate_chance_successor_nodes()
            if len(node.children) == 0:
                node.set_h()
                return node.h_value
            l = []
            for child in node.children:
                # b = min(b, self.minimax_alpha_beta(child, depth-1, a, b, False))
                l.append(self.run_expectimax(child, depth-1, a, b, False))
                node.a = a
                node.b = b

            return reduce(lambda x, y: x + y, l) / len(l)

        # Max function
        elif not chance:
            node.generate_max_successor_nodes()
            if len(node.children) == 0:
                node.set_h()
                return node.h_value
            for child in node.children:
                a = max(a, self.run_expectimax(child, depth-1, a, b, True))
                node.a = a
                node.b = b
            return a

