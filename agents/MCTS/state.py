class State:
    def __init__(self, my_pos, op_pos, board):
        self.my_pos = my_pos
        self.op_pos = op_pos
        self.board = board

    def possible_moves(self):
        return None