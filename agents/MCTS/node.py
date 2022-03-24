from agents.MCTS.state import State


class Node:
    def __init__(self, state: State, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)

    # def available_actions(self):
    #     """
    #     Returns a set of available moves from this node
    #     """
    #     return self.state.possible_moves()
    #
    # def is_terminal(self):
    #     """
    #     Returns true if the node's state is over; false otherwise
    #     """
    #     return self.state.is_over()