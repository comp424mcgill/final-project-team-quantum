import numpy as np


class State:
    def __init__(self, my_pos, op_pos, chess_board):
        self.my_pos = my_pos
        self.op_pos = op_pos
        self.chess_board = chess_board

    def get_next_state(self, next_is_my_turn: bool):
        """
        get the next possible states of the current state
        next_is_my_turn: true if the next turn is mine; false otherwise
        """
        cur_p_pos = self.my_pos[:]
        another_pos = self.op_pos[:]
        if not next_is_my_turn:
            cur_p_pos, another_pos = another_pos, cur_p_pos

        # get the dimensions of the board
        x_list = [-1, 0, 1, 0]
        y_list = [0, 1, 0, -1]
        x_max = self.chess_board.shape[0]
        y_max = self.chess_board.shape[1]
        step_record = np.zeros((x_max, y_max))

        step_record[self.my_pos[0]][self.my_pos[1]] = 1
        step_record[self.op_pos[0]][self.op_pos[1]] = 2
        next_step = [self.my_pos]

        for i in range((self.chess_board.shape[0] + 1) // 2):
            lens = len(next_step)
            for j in range(lens):
                curLoc = next_step.pop(0)
                for k in range(4):  # direction
                    x = curLoc[0] + x_list[k]
                    y = curLoc[1] + y_list[k]
                    if 0 <= x < x_max and 0 <= y < y_max and step_record[x][y] == 0 and not self.chess_board[curLoc[0]][curLoc[1]][k]:
                        step_record[x][y] = 1
                        next_step.append((x, y))

        possible_moves = []
        possible_states = []
        for i in range(x_max):
            for j in range(y_max):
                if step_record[i][j] == 1:
                    for k in range(4):
                        if not self.chess_board[i][j][k]:
                            possible_moves.append(((i, j), k))

                            possible_states.append(State(self.my_ops, self.op_pos, self.chess_board))

        return possible_moves