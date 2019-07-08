#!/usr/bin/env/ python3
import time

X, O, NONE = ("X", "O", ".")


class Board():
    def __init__(self):
        self.board_length = 9;
        self.squares = [NONE for idx in range(self.board_length)]
        self.winning_combinations = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]]

    def __str__(self):
        return  ("-------------\n| {} | {} | {} |\n" * 3 + "-------------").format(*self.squares)

    def make_move(self, location, player):
        if self.is_valid_move(location):
            self.squares[location] = player
            return True
        return False

    def undo_move(self, location):
        if self.is_valid_location(location):
            self.squares[location] = NONE
            return True
        return False

    def is_valid_move(self, location):
        return self.is_valid_location(location) and self.squares[location] == NONE

    def is_valid_location(self, location):
        return location >= 0 and location < self.board_length

    def get_winner(self):
        for player in (X, O):
            for combo in self.winning_combinations:
                if self.squares[combo[0]] == player and self.squares[combo[1]] == player and self.squares[combo[2]] == player:
                    return player
        return NONE

    def get_moves(self):
        return filter(self.is_valid_move, range(9))

iters = 0
def find_winners(board, depth=0, player=X):
    global iters
    iters += 1
    for move in board.get_moves():
        board.make_move(move, player)
        if board.get_winner() == X:
            #print(board)
            _ = 1
        else:
            find_winners(board, depth + 1, O if player == X else X)
        board.undo_move(move)

if __name__ == "__main__":
    start = time.time()
    find_winners(Board())
    print("Took: {time:.4f} seconds to execute {iters} times.".format(time=(time.time() - start), iters=iters))
