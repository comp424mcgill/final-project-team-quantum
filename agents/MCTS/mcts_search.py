import math
import random

from agents.MCTS.node import Node


class MCTS:
    def __init__(self, my_pos, adv_pos, root_board):
        # create the root
        self.root_node = Node(my_pos, adv_pos, 0, -1)
        self.root_board = root_board
        self.cur_node = self.root_node
        self.cur_board = root_board[:][:][:]

    def update_tree(self, new_adv_pos, new_board):
        self.root_node = self.find_children_node(new_adv_pos, new_board)
        self.root_board = new_board[:][:][:]
        self.cur_board = new_board[:][:][:]
        return

    def find_children_node(self, new_adv_pos, new_board):
        """function to find next node according to adv_move"""
        direction = 0
        for i in range(4):
            if new_board[new_adv_pos[0]][new_adv_pos[1]][i] != self.root_board[new_adv_pos[0]][new_adv_pos[1]][i]:
                direction = i
                break
        for node in self.root_node.children:
            if node.op_pos == new_adv_pos and node.dir_barrier == direction:
                return node

    def update_cur_board(self, cur_node):
        # update the current chess board according to the current node
        pass

    def search(self, search_time):
        for i in range(search_time):
            # Select, Rollout, Backpropagation
            selected_node = self.select(self.cur_node)
            score = self.rollout(selected_node)
            self.backpropagate(selected_node, score)

        best_node = self.root_node.children[0]
        max_visit = 0
        for node in self.root_node.children:
            if node.visits > max_visit:
                best_node = node
        return best_node.my_pos, best_node.dir_barrier



    def select(self, node: Node):
        while not node.get_game_result(self.cur_board)['is_my_win']:
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

    def rollout(self, node: Node):
        # do rollout until the node is terminal
        while not node.get_game_result(self.cur_board)['is_my_win']:
            next_node = random.choice(node.get_next_state(self.cur_board))
            self.update_cur_board(next_node)
            node = next_node

        result = node.get_game_result(self.cur_board)
        if result['my_score'] > result['adv_score']:
            return 1
        elif result['my_score'] == result['adv_score']:
            return 0.5
        else:
            return 0


    def backpropagate(self, node: Node, score: float):
        while node is not None:
            # update the node's reward and visits
            node.reward += score
            node.visits += 1

            # goes to the node's parent
            node = node.parent
