import math
import random
import time

from agents.MCTS.node import Node


class MCTS:
    def __init__(self, my_pos, adv_pos, root_board):
        # create the root
        self.root_node = Node(my_pos, adv_pos, False, -1)
        self.cur_node = self.root_node
        self.cur_board = root_board

        # Moves (Up, Right, Down, Left)
        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        # Opposite Directions
        self.opposites = {0: 2, 1: 3, 2: 0, 3: 1}

    """reselect the root node after adv move, update the new board"""
    def update_tree(self, new_adv_pos, new_board):
        self.root_node = self.find_adv_node(new_adv_pos, new_board)
        self.cur_node = self.root_node
        self.cur_board = new_board
        return

    def search(self, search_time):
        start_time = time.time()
        stimulate_time = 0
        while time.time() - start_time <= search_time:
            # Select, Rollout, Backpropagation
            stimulate_time += 1
            score = self.game_play()
            self.backpropagate(score)
            # reset the current board
            self.cur_node = self.root_node

        best_node = self.root_node.children[0]
        max_visit = 0
        # print("stimulate_time:", stimulate_time)
        # print(len(self.root_node.children))
        for node in self.root_node.children:
            # print("Visit:", node.visits, "Reward:", node.reward, "Pos:", node.my_pos)
            if node.visits > max_visit and node.reward > 0:
                max_visit = node.visits
                best_node = node
        # print("max visit", max_visit)

        self.root_node = best_node
        self.cur_node = self.root_node
        self.update_cur_board()
        return best_node.my_pos, best_node.dir_barrier

    def game_play(self):
        game_result = self.cur_node.get_game_result(self.cur_board)
        max_depth = 0
        while not game_result[0] and max_depth < 40:
            # if if's visited
            max_depth += 1
            if self.cur_node.visits != 0:
                self.cur_node = self.select_best_move()
            else:
                self.cur_node = self.expand()
                # print("Pos:", self.cur_node.)
            self.update_cur_board()
            game_result = self.cur_node.get_game_result(self.cur_board)
        # if (max_depth>40):
        #     print("max_depth:", max_depth)
        if game_result[1] > game_result[2]:
            return 1
        elif game_result[1] == game_result[2]:
            return 0.5
        else:
            return 0

    # find adv move according to its new position and new board
    def find_adv_node(self, new_adv_pos, new_board):
        """function to find next node according to adv_move"""
        direction = 0
        for i in range(4):
            if new_board[new_adv_pos[0]][new_adv_pos[1]][i] != self.cur_board[new_adv_pos[0]][new_adv_pos[1]][i]:
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

    def reset_barrier(self, r, c, dir):
        self.cur_board[r, c, dir] = False
        # Set the opposite barrier to False
        move = self.moves[dir]
        self.cur_board[r + move[0], c + move[1], self.opposites[dir]] = False

    def reset_cur_board(self):
        cn = self.cur_node
        if cn.turn:
            self.reset_barrier(cn.my_pos[0], cn.my_pos[1], cn.dir_barrier)
        else:
            self.reset_barrier(cn.adv_pos[0], cn.adv_pos[1], cn.dir_barrier)

    def expand(self):
        self.cur_node.get_next_state(self.cur_board)
        # print("Children:", len(self.cur_node.children))

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
            self.reset_cur_board()
            # goes to the node's parent
            self.cur_node = self.cur_node.parent

        self.cur_node.reward += score
        self.cur_node.visits += 1
        # goes to the node's parent
