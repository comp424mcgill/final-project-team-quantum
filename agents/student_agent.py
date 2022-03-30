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
        # dummy return
        # moves = self.get_legal_move(chess_board, my_pos, adv_pos, max_step)
        # new_boards = []
        # valid = [1] * len(moves)
        # for i in range(len(moves)):
        #     move = moves[i]
        #     new_chess_board = chess_board.copy()
        #     self.set_barrier(move[0][0], move[0][1], move[1], new_chess_board)
        #     new_boards.append(new_chess_board)
        #     result = self.get_game_result(new_chess_board, move[0], adv_pos)
        #     if result[0] and result[1] > result[2]:
        #         return move
        #     if result[0] and result[2] > result[1]:
        #         valid[i] = 0
        # for i in range(len(moves)):
        #     # print("pm:", moves[i])
        #     if valid[i] == 0:
        #         continue
        #     legal_moves = self.get_legal_move(new_boards[i], adv_pos, moves[i][0], max_step)
        #     # print(legal_moves)
        #     for lm in legal_moves:
        #         new_chess_board1 = new_boards[i].copy()
        #         self.set_barrier(lm[0][0], lm[0][1], lm[1], new_chess_board1)
        #         result = self.get_game_result(new_chess_board1, moves[i][0], lm[0])
        #         if result[0] and result[2] > result[1]:
        #             # print(lm, "Find danger")
        #             valid[i] = 0
        #             break
        # good_moves = []
        # for i in range(len(moves)):
        #     if valid[i] == 1:
        #         good_moves.append(moves[i])
        #
        # if len(good_moves) <= 0:
        #     print("I gave up!!!")
        #     return random.choices(moves, weights=None, k=1)[0]
        # else:
        #     return random.choices(good_moves, weights=None, k=1)[0]

        if self.mcts_tree is None:
            self.mcts_tree = MCTS(my_pos, adv_pos, chess_board)

            return self.mcts_tree.search(28)
        else:
            self.mcts_tree.update_tree(adv_pos, chess_board)
            return self.mcts_tree.search(1.8)

    def set_barrier(self, r, c, dir, board):
        # Set the barrier to True
        opposites = {0: 2, 1: 3, 2: 0, 3: 1}
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        board[r, c, dir] = True
        # Set the opposite barrier to True
        move = moves[dir]
        board[r + move[0], c + move[1], opposites[dir]] = True


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
                    if 0 <= x < x_max and 0 <= y < y_max \
                            and step_record[x][y] == 0 \
                            and not chess_board[curLoc[0]][curLoc[1]][k]:
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
    #
    def get_game_result(self, chess_board, my_pos, adv_pos):
        # get the dimensions of the board
        x_list = [-1, 0, 1, 0]
        y_list = [0, 1, 0, -1]
        x_max = chess_board.shape[0]
        y_max = chess_board.shape[1]
        step_record = np.zeros((x_max, y_max))

        step_record[my_pos[0]][my_pos[1]] = 1
        step_record[adv_pos[0]][adv_pos[1]] = 2
        next_step = [my_pos]

        while len(next_step) > 0:
            lens = len(next_step)
            for j in range(lens):
                curLoc = next_step.pop(0)
                for k in range(4):  # direction
                    if chess_board[curLoc[0]][curLoc[1]][k]:
                        continue

                    x = curLoc[0] + x_list[k]
                    y = curLoc[1] + y_list[k]

                    if 0 <= x < x_max and 0 <= y < y_max:
                        if step_record[x][y] == 2:
                            return False, 0, 0
                        elif step_record[x][y] == 0:
                            step_record[x][y] = 1
                            next_step.append((x, y))

        next_step = [adv_pos]
        # print("next step:", next_step)
        # print(step_record)
        while len(next_step) > 0:
            lens = len(next_step)
            for j in range(lens):
                curLoc = next_step.pop(0)
                for k in range(4):  # direction
                    if chess_board[curLoc[0]][curLoc[1]][k]:
                        continue
                    x = curLoc[0] + x_list[k]
                    y = curLoc[1] + y_list[k]
                    if 0 <= x < x_max and 0 <= y < y_max \
                            and step_record[x][y] == 0:
                        step_record[x][y] = 2
                        next_step.append((x, y))

        my_score = 0
        adv_score = 0
        for i in range(x_max):
            for j in range(y_max):
                if step_record[i][j] == 1:
                    my_score = my_score + 1
                if step_record[i][j] == 2:
                    adv_score = adv_score + 1

        return True, my_score, adv_score
