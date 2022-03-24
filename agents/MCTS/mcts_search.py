from agents.MCTS.node import Node


class MCTS:
    def __init__(self, initial_state):
        # create the root
        self.root = Node(initial_state)

    def search(self, initial_state):
        for i in range(2000):
            # Select, Rollout, Backpropagation
            pass

    def select(self, node):
        while not node.is_terminal:
            # if if's visited
            if node.is_visited:
                node = self.select_best_move(node)
            else:
                node = self.expand(node)
        return node

    def expand(self, node):
        pass

    def select_best_move(self, node):
        pass
