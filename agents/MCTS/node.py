import numpy as np
import random

class Node:
    def __init__(self, my_pos, adv_pos, turn, dir_barrier, parent=None):
        self.my_pos = my_pos
        self.adv_pos = adv_pos
        self.turn = turn
        self.dir_barrier = dir_barrier

        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0

    def get_info(self):
        print(self.my_pos, self.adv_pos, self.turn, self.dir_barrier, self.visits, self.reward)

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

        max_step = (chess_board.shape[0] + 1) // 2
        for i in range(max_step):
            lens = len(next_step)
            for j in range(lens):
                cur_loc = next_step.pop(0)
                for k in range(4):  # direction
                    x = cur_loc[0] + x_list[k]
                    y = cur_loc[1] + y_list[k]
                    if 0 <= x < x_max and 0 <= y < y_max and step_record[x][y] == 0 and not chess_board[cur_loc[0]][cur_loc[1]][k]:
                        step_record[x][y] = 1
                        next_step.append((x, y))

        for i in range(x_max):
            for j in range(y_max):
                if step_record[i][j] == 1:
                    for k in range(4):
                        if not chess_board[i][j][k]:
                            if self.turn:
                                self.children.append(Node(self.my_pos[:], (i, j), not self.turn, k, self))
                            else:
                                self.children.append(Node((i, j), self.adv_pos[:], not self.turn, k, self))
        random.shuffle(self.children)
        return

    def get_game_result(self, chess_board):
        my_pos = self.my_pos
        adv_pos = self.adv_pos
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
                    # check if the direction can move
                    if chess_board[curLoc[0]][curLoc[1]][k]:
                        continue

                    x = curLoc[0] + x_list[k]
                    y = curLoc[1] + y_list[k]

                    if 0 <= x < x_max and 0 <= y < y_max:
                        if step_record[x][y] == 2:  # meet adv
                            return {0: False, 1: 0, 2: 0}
                        elif step_record[x][y] == 0:
                            step_record[x][y] = 1
                            next_step.append((x, y))

        next_step = [adv_pos]
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

        return {0: True, 1: my_score, 2: adv_score}

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