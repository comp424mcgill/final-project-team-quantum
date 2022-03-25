import math
import random

from agents.MCTS.node import Node


class MCTS:
    def __init__(self, my_pos, adv_pos, turn, dir_barrier, root_board):
        # create the root
        self.root_node = Node(my_pos, adv_pos, turn, dir_barrier)
        self.root_board = root_board
        # self.cur_node = self.root_node
        self.cur_board = root_board[:][:][:]

    def update_tree(self, new_my_pos, new_adv_pos, turn, dir_barrier, new_board):
        move = self.get_adv_move(new_my_pos, new_adv_pos, new_board)
        self.root_node = self.find_children_node(move)
        self.root_board = new_board
        self.cur_board = new_board[:][:][:]
        return

    def get_adv_move(self, new_my_pos, new_adv_pos, new_board):
        """function to calculate move according to new board and position"""
        return

    def find_children_node(self, move):
        """function to find next node according to adv_move"""
        return

    def find_best_child(self):
        pass

    def update_cur_board(self, cur_node):
        # update the current chess board according to the current node
        pass

    def search(self):
        for i in range(2000):
            # Select, Rollout, Backpropagation
            selected_node = self.select(self.root_node)
            pass

    def select(self, node: Node):
        while not node.get_game_result(self.cur_board):
            # if if's visited
            if node.is_visited:
                node = self.select_best_move(node)
            else:
                node = self.expand(node)
            self.update_cur_board(node)

        self.update_cur_board(node)
        return node

    def expand(self, node: Node):
        node.get_next_state(self.cur_board)
        return node.children[0]

    def select_best_move(self, node: Node):
        """function to select the best node"""
        best_score = float('-inf')
        best_moves = []

        for cn in node.children:
            score_flag = 1 if cn.turn else -1

            # use UCT formula to calculate the score
            child_node_score = score_flag*cn.reward/cn.visits + math.sqrt(2*math.log(node.visits/cn.visits))

            # update the best score and the list of best moves
            if child_node_score > best_score:
                best_score = child_node_score
                best_moves = [cn]
            elif child_node_score == best_score:
                best_moves.append(cn)

        return random.choice(best_moves)

    def rollout(self):
        pass
