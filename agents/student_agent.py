# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import numpy as np


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
        # dummy return
        possible_steps = self.get_legal_move(chess_board, my_pos, adv_pos, max_step)
        print(possible_steps)
        return possible_steps[0][0], possible_steps[0][1]

    def get_legal_move(self, chess_board, my_pos, adv_pos, max_step):
        # get the dimensions of the board
        x_list = [-1, 0, 1, 0]
        y_list = [0, 1, 0, -1]
        x_max = chess_board.shape[0]
        y_max = chess_board.shape[1]
        step_record = np.zeros((x_max, y_max))

        step_record[my_pos[0]][my_pos[1]] = 1
        step_record[adv_pos[0]][adv_pos[1]] = 2
        next_step = [my_pos]

        for i in range(max_step):
            lens = len(next_step)
            for j in range(lens):
                curLoc = next_step.pop(0)
                for k in range(4):  # direction
                    x = curLoc[0] + x_list[k]
                    y = curLoc[1] + y_list[k]
                    if 0 <= x < x_max and 0 <= y < y_max and step_record[x][y] == 0 and not chess_board[curLoc[0]][curLoc[1]][k]:
                        step_record[x][y] = 1
                        next_step.append((x, y))

        possible_moves = []
        for i in range(x_max):
            for j in range(y_max):
                if step_record[i][j] == 1:
                    for k in range(4):
                        if not chess_board[i][j][k]:
                            possible_moves.append(((i, j), k))

        return possible_moves
