import numpy as np
from copy import deepcopy
from agents.agent import Agent
from store import register_agent
import random
# Important: you should register your agent with a name
def get_legal_move(chess_board, my_pos, adv_pos, max_step):
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


@register_agent("random_agent")
class RandomAgent(Agent):
    """
    Example of an agent which takes random decisions
    """

    def __init__(self):
        super(RandomAgent, self).__init__()
        self.name = "RandomAgent"
        self.autoplay = True

    def step(self, chess_board, my_pos, adv_pos, max_step):

        moves = get_legal_move(chess_board, my_pos, adv_pos, max_step)
        new_boards = []
        valid = [1] * len(moves)
        for i in range(len(moves)):
            move = moves[i]
            new_chess_board = chess_board.copy()
            self.set_barrier(move[0][0], move[0][1], move[1], new_chess_board)
            new_boards.append(new_chess_board)
            result = self.get_game_result(new_chess_board, move[0], adv_pos)
            if result[0] and result[1] > result[2]:
                return move
            if result[0] and result[2] > result[1]:
                valid[i] = 0
        for i in range(len(moves)):
            # print("pm:", moves[i])
            if valid[i] == 0:
                continue
            legal_moves = get_legal_move(new_boards[i], adv_pos, moves[i][0], max_step)
            # print(legal_moves)
            for lm in legal_moves:
                new_chess_board1 = new_boards[i].copy()
                self.set_barrier(lm[0][0], lm[0][1], lm[1], new_chess_board1)
                result = self.get_game_result(new_chess_board1, moves[i][0], lm[0])
                if result[0] and result[2] > result[1]:
                    # print(lm, "Find danger")
                    valid[i] = 0
                    break
        good_moves = []
        for i in range(len(moves)):
            if valid[i] == 1:
                good_moves.append(moves[i])

        if len(good_moves) <= 0:
            print("I gave up!!!")
            return random.choices(moves, weights=None, k=1)[0]
        else:
            return random.choices(good_moves, weights=None, k=1)[0]
        # Moves (Up, Right, Down, Left)
        # ori_pos = deepcopy(my_pos)
        # moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        # steps = np.random.randint(0, max_step + 1)
        #
        # # Random Walk
        # for _ in range(steps):
        #     r, c = my_pos
        #     dir = np.random.randint(0, 4)
        #     m_r, m_c = moves[dir]
        #     my_pos = (r + m_r, c + m_c)
        #
        #     # Special Case enclosed by Adversary
        #     k = 0
        #     while chess_board[r, c, dir] or my_pos == adv_pos:
        #         k += 1
        #         if k > 300:
        #             break
        #         dir = np.random.randint(0, 4)
        #         m_r, m_c = moves[dir]
        #         my_pos = (r + m_r, c + m_c)
        #
        #     if k > 300:
        #         my_pos = ori_pos
        #         break
        #
        # # Put Barrier
        # dir = np.random.randint(0, 4)
        # r, c = my_pos
        # while chess_board[r, c, dir]:
        #     dir = np.random.randint(0, 4)
        #
        # return my_pos, dir

    #
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
    def set_barrier(self, r, c, dir, board):
        # Set the barrier to True
        opposites = {0: 2, 1: 3, 2: 0, 3: 1}
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        board[r, c, dir] = True
        # Set the opposite barrier to True
        move = moves[dir]
        board[r + move[0], c + move[1], opposites[dir]] = True

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

