
class Minimax():
    # returns terminal value, return the best value for max, best value for minimax
    def __init__(self):
        return

    def minimax_alpha_beta(self, node, depth, a, b, direction):
        if depth == 0:
            node.set_h()
            return node.h_value

        if direction==None:
            r = node.generate_max_successor_nodes()
            if len(r) == 0 or r == None:
                return None
            left = right = up = down = None
            for child in node.children:
                if child.move == "left":
                    left = max(a, self.minimax_alpha_beta(child, depth-1, a, b, True))
                elif child.move == "right":
                    right = max(a, self.minimax_alpha_beta(child, depth-1, a, b, True))
                elif child.move == "up":
                    up = max(a, self.minimax_alpha_beta(child, depth-1, a, b, True))
                elif child.move == "down":
                    down = max(a, self.minimax_alpha_beta(child, depth-1, a, b, True))

            # print "left: " + str(left)
            # print "right: " + str(right)
            # print "up: " + str(up)
            # print "down: " + str(down)
            # TODO return max of left, right, up, down
            result =  max(left,right,up,down)
            if result==left:
                return "left"
            elif result==right:
                return "right"
            elif result==up:
                return "up"
            elif result==down:
                return "down"

        # Min function
        elif direction:
            # this is a left, right, up, down node
            # generate min successors and returns the average value
            # a = -inf, b = inf
            node.generate_min_successor_nodes()
            if len(node.children) == 0:
                node.set_h()
                return node.h_value
            l = []
            for child in node.children:
                # b = min(b, self.minimax_alpha_beta(child, depth-1, a, b, False))
                l.append(self.minimax_alpha_beta(child, depth-1, a, b, False))
                node.a = a
                node.b = b

            return reduce(lambda x, y: x + y, l) / len(l)
            #return b

        # Max function
        elif not direction:
            node.generate_max_successor_nodes()
            if len(node.children) == 0:
                node.set_h()
                return node.h_value
            for child in node.children:
                a = max(a, self.minimax_alpha_beta(child, depth-1, a, b, True))
                node.a = a
                node.b = b
            return a

