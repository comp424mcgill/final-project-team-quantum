import math
import random

from agents.MCTS.node import Node


class MCTS:
    def __init__(self, my_pos, adv_pos, root_board):
        # create the root
        self.root_node = Node(my_pos, adv_pos, False, -1)
        self.root_board = root_board.copy()
        self.cur_node = self.root_node
        self.cur_board = root_board.copy()

        # Moves (Up, Right, Down, Left)
        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        # Opposite Directions
        self.opposites = {0: 2, 1: 3, 2: 0, 3: 1}

    def update_tree(self, new_adv_pos, new_board):
        self.root_node = self.find_children_node(new_adv_pos, new_board)
        self.cur_node = self.root_node
        self.root_board = new_board.copy()
        self.cur_board = new_board.copy()
        return

    def find_children_node(self, new_adv_pos, new_board):
        """function to find next node according to adv_move"""
        direction = 0
        for i in range(4):
            if new_board[new_adv_pos[0]][new_adv_pos[1]][i] != self.root_board[new_adv_pos[0]][new_adv_pos[1]][i]:
                direction = i
                break
        for node in self.root_node.children:
            if node.adv_pos == new_adv_pos and node.dir_barrier == direction:
                return node

    def set_barrier(self, r, c, dir):
        # Set the barrier to True
        self.cur_board[r, c, dir] = True
        # Set the opposite barrier to True
        move = self.moves[dir]
        self.cur_board[r + move[0], c + move[1], self.opposites[dir]] = True

    def update_cur_board(self):
        # update the current chess board according to the current node
        cn = self.cur_node
        if cn.turn:
            self.set_barrier(cn.my_pos[0], cn.my_pos[1], cn.dir_barrier)
        else:
            self.set_barrier(cn.adv_pos[0], cn.adv_pos[1], cn.dir_barrier)

    def set_root_barrier(self, r, c, dir):
        # Set the barrier to True
        self.root_board[r, c, dir] = True
        # Set the opposite barrier to True
        move = self.moves[dir]
        self.root_board[r + move[0], c + move[1], self.opposites[dir]] = True

    def update_root_board(self, best_node):
        # update the current chess board according to the current node
        cn = best_node
        if cn.turn:
            self.set_root_barrier(cn.my_pos[0], cn.my_pos[1], cn.dir_barrier)
        else:
            self.set_root_barrier(cn.adv_pos[0], cn.adv_pos[1], cn.dir_barrier)

    def search(self, search_time):
        for i in range(search_time):
            # Select, Rollout, Backpropagation
            score = self.select()
            self.backpropagate(score)
            # reset the current board
            self.cur_board = self.root_board.copy()
            self.cur_node = self.root_node

        best_node = self.root_node.children[0]
        max_visit = 0
        for node in self.root_node.children:
            if node.visits > max_visit:
                best_node = node

        self.root_node = best_node
        self.cur_node = self.root_node
        self.update_root_board(best_node)
        self.cur_board = self.root_board.copy()
        return best_node.my_pos, best_node.dir_barrier

    def select(self):
        game_result = self.cur_node.get_game_result(self.cur_board)
        while not game_result[0]:
            # if if's visited
            if self.cur_node.visits != 0:
                self.cur_node = self.select_best_move()
            else:
                self.cur_node = self.expand()
            self.update_cur_board()
            game_result = self.cur_node.get_game_result(self.cur_board)
        if game_result[1] > game_result[2]:
            return 1
        elif game_result[1] == game_result[2]:
            return 0.5
        else:
            return 0

    def expand(self):
        self.cur_node.get_next_state(self.cur_board)
        return self.cur_node.children[0]

    def select_best_move(self):
        """function to select the best node"""
        best_score = float('-inf')
        best_moves = []

        for cn in self.cur_node.children:
            score_flag = 1 if cn.turn else -1

            # use UCT formula to calculate the score
            if cn.visits == 0:
                child_node_score = math.inf
            else:
                child_node_score = score_flag*cn.reward/cn.visits + math.sqrt(2*math.log(self.cur_node.visits/cn.visits))

            # update the best score and the list of best moves
            if child_node_score > best_score:
                best_score = child_node_score
                best_moves = [cn]
            elif child_node_score == best_score:
                best_moves.append(cn)

        return random.choice(best_moves)

    def backpropagate(self, score: float):
        while self.cur_node != self.root_node:
            # update the node's reward and visits
            self.cur_node.reward += score
            self.cur_node.visits += 1

            # goes to the node's parent
            self.cur_node = self.cur_node.parent
