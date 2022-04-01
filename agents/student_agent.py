# Student agent: Add your own agent here
from agents.MCTS.mcts_search import MCTS
from agents.agent import Agent
from store import register_agent
import numpy as np
import random


@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }
        self.mcts_tree = None

    def step(self, chess_board, my_pos, adv_pos, max_step):
        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """

        if self.mcts_tree is None:  # initiate the tree
            self.mcts_tree = MCTS(my_pos, adv_pos, chess_board)
            return self.mcts_tree.search(2)
        else:
            self.mcts_tree.update_tree(adv_pos, chess_board)
            return self.mcts_tree.search(1.8)

