import numpy as np
import random
from copy import deepcopy


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
        self.max_children = 0  # impossible number
        random.seed(0)

    """function to print out the infomation of a node"""
    def get_info(self):
        print(self.my_pos, self.adv_pos, self.turn, self.dir_barrier, self.visits, self.reward)

    """ random select a possible move from current node"""
    def get_one_child(self, chess_board):
        max_step = (chess_board.shape[0] + 1) // 2

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        oppsite = {(-1, 0): (1, 0), (0, 1): (0, -1), (1, 0): (-1, 0), (0, -1): (0, 1), (0, 0): (0, 0)}
        steps = np.random.randint(0, max_step + 1)
        if self.turn:
            next_pos = deepcopy(self.adv_pos)
            adv_pos = deepcopy(self.my_pos)
        else:
            next_pos = deepcopy(self.my_pos)
            adv_pos = deepcopy(self.adv_pos)
        last_move = (0, 0)

        """find a random location that can be reached"""
        for _ in range(steps):
            r, c = next_pos
            possible_move = []
            for i in range(4):
                move = moves[i]
                if not chess_board[r, c, i] and (r + move[0], c + move[1]) != adv_pos and move != oppsite[last_move]:
                    possible_move.append(move)
            if len(possible_move) > 0:
                last_move = random.choice(possible_move)
            else:
                break
            next_pos = (r + last_move[0], c + last_move[1])
        """find one possible barrier to put"""
        possible_dir = []
        for dirc in range(4):
            if not chess_board[next_pos[0], next_pos[1], dirc]:
                possible_dir.append(dirc)
        next_dir = random.choice(possible_dir)

        """check if the move is already existed in the children"""
        for node in self.children:
            if node.turn:
                if next_pos[0] == node.adv_pos[0] and next_pos[1] == node.adv_pos[1] and next_dir == node.dir_barrier:
                    return node
            else:
                if next_pos[0] == node.my_pos[0] and next_pos[1] == node.my_pos[1] and next_dir == node.dir_barrier:
                    return node

        if self.turn:
            new_node = Node(self.my_pos[:], next_pos[:], not self.turn, next_dir, self)
        else:
            new_node = Node(next_pos[:], self.adv_pos[:], not self.turn, next_dir, self)
        self.children.append(new_node)
        return new_node

    def get_next_state(self, chess_board, shrink):
        """
        get the next possible states of the current state
        turn: true if the next turn is mine; false otherwise
        """
        x_list = [-1, 0, 1, 0]
        y_list = [0, 1, 0, -1]
        cur_p_pos = self.my_pos[:]
        another_pos = self.adv_pos[:]
        # exchange position if it is
        if self.turn:
            cur_p_pos, another_pos = another_pos, cur_p_pos

        if shrink < 4:
            shrink = 1

        """get the dimensions of the board"""
        x_max = chess_board.shape[0]
        y_max = chess_board.shape[1]
        max_step = (chess_board.shape[0] + 1) // 2

        step_record = np.zeros((x_max, y_max))  # record the position that have been taken
        step_record[cur_p_pos[0]][cur_p_pos[1]] = 1
        step_record[another_pos[0]][another_pos[1]] = 2
        next_step = [cur_p_pos]  # start iterate through the first position

        for i in range(max_step):  # Find max_step iterations for the steps
            lens = len(next_step)  # how many possible position to extend
            for j in range(lens):
                cur_loc = next_step.pop(0)
                for k in range(4):  # direction
                    x = cur_loc[0] + x_list[k]  # new position for moving one step
                    y = cur_loc[1] + y_list[k]
                    if 0 <= x < x_max and 0 <= y < y_max and step_record[x][y] == 0 and not \
                            chess_board[cur_loc[0]][cur_loc[1]][k]:  # check if the move is legitimate
                        step_record[x][y] = 1
                        next_step.append((x, y))
        childrens = []
        for i in range(x_max):  # find all possible positions from my position
            for j in range(y_max):
                if step_record[i][j] == 1:
                    for k in range(4):  # find possible barrier dir to add
                        if not chess_board[i][j][k]:
                            if self.turn:
                                childrens.append(Node(self.my_pos[:], (i, j), not self.turn, k, self))
                            else:
                                childrens.append(Node((i, j), self.adv_pos[:], not self.turn, k, self))
        # reshuffle the children to make sure a random child is selected
        random.shuffle(childrens)
        # print("new length", len(childrens[len(self.children):len(self.children)+length]))
        self.children.extend(childrens[len(self.children):len(self.children) + len(childrens) // shrink + 2])
        self.max_children = len(childrens)
        return

    def get_game_result(self, chess_board):
        """
        get the game result of the chess_board according to the chess_board
        return 0: True/False Game end, 1: Score for My_pos, Score for Adv.Pos
        """
        x_list = [-1, 0, 1, 0]
        y_list = [0, 1, 0, -1]
        my_pos = self.my_pos
        adv_pos = self.adv_pos
        # get the dimensions of the board
        x_max = chess_board.shape[0]
        y_max = chess_board.shape[1]
        step_record = np.zeros((x_max, y_max))

        step_record[my_pos[0]][my_pos[1]] = 1
        step_record[adv_pos[0]][adv_pos[1]] = 2
        next_step = [my_pos]

        while len(next_step) > 0:  # find all possible areas that can be reached by My_pos
            lens = len(next_step)
            for j in range(lens):
                cur_loc = next_step.pop(0)
                for k in range(4):  # direction
                    # check if the direction can move
                    if chess_board[cur_loc[0]][cur_loc[1]][k]:
                        continue
                    x = cur_loc[0] + x_list[k]
                    y = cur_loc[1] + y_list[k]

                    if 0 <= x < x_max and 0 <= y < y_max:
                        if step_record[x][y] == 2:  # meet adv
                            return {0: False, 1: 0, 2: 0}  # both in the same area, game not end
                        elif step_record[x][y] == 0:
                            step_record[x][y] = 1
                            next_step.append((x, y))

        next_step = [adv_pos]  # find possible moves for adv position
        while len(next_step) > 0:
            lens = len(next_step)
            for j in range(lens):
                cur_loc = next_step.pop(0)
                for k in range(4):  # direction
                    if chess_board[cur_loc[0]][cur_loc[1]][k]:
                        continue
                    x = cur_loc[0] + x_list[k]
                    y = cur_loc[1] + y_list[k]
                    if 0 <= x < x_max and 0 <= y < y_max \
                            and step_record[x][y] == 0:
                        step_record[x][y] = 2
                        next_step.append((x, y))

        my_score = 0
        adv_score = 0
        #   find area for my_pos and adv_pos
        for i in range(x_max):
            for j in range(y_max):
                if step_record[i][j] == 1:
                    my_score = my_score + 1
                if step_record[i][j] == 2:
                    adv_score = adv_score + 1

        return {0: True, 1: my_score, 2: adv_score}
