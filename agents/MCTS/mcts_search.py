import math
import random
import time
import gc


from agents.MCTS.node import Node


class MCTS:
    def __init__(self, my_pos, adv_pos, root_board):
        # create the root
        self.root_node = Node(my_pos, adv_pos, False, -1)
        self.cur_node = self.root_node
        self.cur_board = root_board

        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))  # Moves (Up, Right, Down, Left)
        self.opposites = {0: 2, 1: 3, 2: 0, 3: 1}  # Opposite Directions

    """reselect the root node after adv move, update the new board"""
    def update_tree(self, new_adv_pos, new_board):
        self.expand(1)
        self.root_node = self.find_adv_node(new_adv_pos, new_board)
        self.cur_node = self.root_node
        self.cur_board = new_board
        return

    """stimulate the game to develop the tree"""
    def search(self, search_time):
        start_time = time.time()
        stimulate_time = 0

        self.expand(1)
        for child in self.root_node.children:
            self.cur_node = child
            self.update_cur_board()
            result = child.get_game_result(self.cur_board)
            if result[0] and result[1] > result[2]:
                self.root_node = child  # update the tree and board according to the best move
                return child.my_pos, child.dir_barrier
            # self.expand(1)
            # for grandson in child.children:
            #     self.cur_node = grandson
            #     self.update_cur_board()
            #     result = child.get_game_result(self.cur_board)
            #     if result[0] and result[1] < result[2]:
            #         self.cur_node.parent.reward = -10000
            #         self.reset_cur_board()
            #         break
            #     self.reset_cur_board()
            # self.cur_node = self.cur_node.parent
            self.reset_cur_board()
        self.cur_node = self.root_node
    #   print("time to cal:", time.time()-start_time)

        while time.time() - start_time <= search_time:
            stimulate_time += 1
            score = self.game_play()    # start the stimulation of a game
            self.backpropagate(score)   # update the result of this stimulation
            self.cur_node = self.root_node  # reset the current node

        best_node = self.root_node.children[0]
        max_visit = 0
        for node in self.root_node.children:    # find the most visited node
            # print("Visit:", node.visits, "Reward:", node.reward, "Pos:", node.my_pos)
            if node.visits > max_visit and node.reward > 0:
                max_visit = node.visits
                best_node = node
        print("max visit:", max_visit, "max_reward", best_node.reward)
        print("Stimulate time:", stimulate_time)
        self.root_node = best_node  # update the tree and board according to the best move
        self.cur_node = self.root_node
        self.update_cur_board()
        print("time to return:", time.time()-start_time)

        return best_node.my_pos, best_node.dir_barrier

    def game_play(self):

        game_result = self.cur_node.get_game_result(self.cur_board)
        shrink_factor = 1
        depth = 0
        flag = False
        self.expand(1)
        self.cur_node = self.select_best_move()
        self.update_cur_board()
        while not game_result[0]:
            # if it's visited
            new_pos, new_dir = self.cur_node.get_one_child(self.cur_board)
            for node in self.cur_node.children:
                if node.turn:
                    if new_pos[0] == node.adv_pos[0] and new_pos[1] == node.adv_pos[1] and new_dir == node.dir_barrier:
                        self.cur_node = node
                        self.update_cur_board()
                        flag = True
                        break
                else:
                    if new_pos[0] == node.my_pos[0] and new_pos[1] == node.my_pos[1] and new_dir == node.dir_barrier:
                        self.cur_node = node
                        self.update_cur_board()
                        flag = True
                        break
            if not flag:
                if self.cur_node.turn:
                    new_node = Node(self.cur_node.my_pos[:], new_pos[:], not self.cur_node.turn, new_dir, self.cur_node)
                else:
                    new_node = Node(new_pos[:], self.cur_node.adv_pos[:], not self.cur_node.turn, new_dir, self.cur_node)
                self.cur_node = new_node
                self.update_cur_board()
            # if self.cur_node.visits == 0 or len(self.cur_node.children) <= self.cur_node.visits < self.cur_node.max_children:
            #     self.expand(shrink_factor)
            # shrink_factor *= 2
            # depth += 1
            # self.cur_node = self.select_best_move()
            # self.update_cur_board()
            game_result = self.cur_node.get_game_result(self.cur_board)

        if game_result[1] > game_result[2]:
            return 1
        elif game_result[1] == game_result[2]:
            return 0.5
        else:
            return 0

    """function to find next node according to adv_move"""
    def find_adv_node(self, new_adv_pos, new_board):
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

    def expand(self, shrink_factor):
        self.cur_node.get_next_state(self.cur_board, shrink_factor)
        return

    """function to select the best node"""
    def select_best_move(self):
        best_score = float('-inf')
        best_moves = []

        for cn in self.cur_node.children:
            score_flag = 1 if cn.turn else -1
            # use UCT formula to calculate the score
            if cn.visits == 0:
                child_node_score = math.inf
            else:
                child_node_score = score_flag * cn.reward / cn.visits + math.sqrt(
                    2 * math.log(self.cur_node.visits / cn.visits))

            # update the best score and the list of best moves
            if child_node_score > best_score:
                best_score = child_node_score
                best_moves = [cn]
            elif child_node_score == best_score and cn.reward >= 0:
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

        self.cur_node.reward += score   # update the root
        self.cur_node.visits += 1
