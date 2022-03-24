import numpy as np


class State:
    def __init__(self, my_pos, adv_pos, turn, dir_barrier):
        self.my_pos = my_pos
        self.op_pos = adv_pos
        self.turn = turn
        self.dir_barrier = dir_barrier

    def get_next_state(self, chess_board):
        """
        get the next possible states of the current state
        turn: true if the next turn is mine; false otherwise
        """
        cur_p_pos = self.my_pos[:]
        another_pos = self.adv_pos[:]
        if self.turn:
            cur_p_pos, another_pos = another_pos, cur_p_pos

        # get the dimensions of the board
        x_list = [-1, 0, 1, 0]
        y_list = [0, 1, 0, -1]
        x_max = chess_board.shape[0]
        y_max = chess_board.shape[1]
        step_record = np.zeros((x_max, y_max))

        step_record[cur_p_pos[0]][cur_p_pos[1]] = 1
        step_record[another_pos[0]][another_pos[1]] = 2
        next_step = [cur_p_pos]

        for i in range((chess_board.shape[0] + 1) // 2):
            lens = len(next_step)
            for j in range(lens):
                cur_loc = next_step.pop(0)
                for k in range(4):  # direction
                    x = cur_loc[0] + x_list[k]
                    y = cur_loc[1] + y_list[k]
                    if 0 <= x < x_max and 0 <= y < y_max and step_record[x][y] == 0 and not chess_board[cur_loc[0]][cur_loc[1]][k]:
                        step_record[x][y] = 1
                        next_step.append((x, y))

        possible_states = []
        for i in range(x_max):
            for j in range(y_max):
                if step_record[i][j] == 1:
                    for k in range(4):
                        if not chess_board[i][j][k]:
                            if self.turn:
                                possible_states.append(State(self.my_ops, (i, j), not self.turn, k))
                            else:
                                possible_states.append(State((i, j), self.adv_pos, not self.turn, k))

        return possible_states

    def is_terminal(self):
        pass