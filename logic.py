import numpy as np


class TicTacToe:
    def __init__(self):
        self.board = [['', '', ''],
                      ['', '', ''],
                      ['', '', '']]
        self.was_cross = False

    def get_place(self, row, col):
        if self.was_cross:
            self.was_cross = False
            self.board[row][col] = 'O'
            return 'O'
        else:
            self.was_cross = True
            self.board[row][col] = 'X'
            return 'X'

    @staticmethod
    def checkRows(board):
        for row in board:
            if len(set(row)) == 1:
                return row[0]
        return 0

    @staticmethod
    def checkDiagonals(board):
        if len(set([board[i][i] for i in range(len(board))])) == 1:
            return board[0][0]
        if len(set([board[i][len(board) - i - 1] for i in range(len(board))])) == 1:
            return board[0][len(board) - 1]
        return 0

    def is_win(self):
        # transposition to check rows, then columns
        temp_board = self.board
        for newBoard in [temp_board, np.transpose(np.array(temp_board))]:
            result = self.checkRows(newBoard)
            if result:
                return result
        return self.checkDiagonals(temp_board)
