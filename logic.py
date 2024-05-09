import json
import random

import numpy as np

from client import HostingClient


class TicTacToe:
    def __init__(self, host):
        self.host = host
        self.board = [['', '', ''],
                      ['', '', ''],
                      ['', '', '']]
        my_number = random.random()
        self._send_data({'turn': my_number})
        while self.host.turn is None:
            continue
        if self.host.turn > my_number:
            self.is_you_cross = False
        elif self.host.turn < my_number:
            self.is_you_cross = True
        elif isinstance(self.host, HostingClient):
            self.is_you_cross = True
        else:
            self.is_you_cross = False
        print(self.is_you_cross)
        self.was_cross = False
    def _send_data(self, data:dict):
        if isinstance(self.host, HostingClient):
            self.host.connection.send(json.dumps(data).encode('utf-8'))
        else:
            try:
                self.host.server_socket.send(json.dumps(data).encode('utf-8'))
            except Exception as e:
                print(e)
                exit()
    def get_place(self, row, col):
        if self.was_cross and not self.is_you_cross:
            self.was_cross = False
            self.board[row][col] = 'O'
            self._send_data({'row': row, 'col': col})
            return 'O'
        elif not self.was_cross and self.is_you_cross:
            self.was_cross = True
            self.board[row][col] = 'X'
            self._send_data({'row': row, 'col': col})
            return 'X'
        return None
    def get_update(self):
        if self.host.row is not None and self.host.col is not None:
            if self.was_cross and self.is_you_cross:
                self.was_cross = False
                self.board[self.host.row][self.host.col] = 'O'
                data = {'row': self.host.row, 'col': self.host.col, 'letter': 'O'}
                self.host.row, self.host.col = None, None
                return data
            if not self.was_cross and not self.is_you_cross:
                self.was_cross = True
                self.board[self.host.row][self.host.col] = 'X'
                data = {'row': self.host.row, 'col': self.host.col, 'letter': 'X'}
                self.host.row, self.host.col = None, None
                return data
        return None

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
        temp_board = self.board.copy()
        for newBoard in [temp_board, np.transpose(np.array(temp_board))]:
            result = self.checkRows(newBoard)
            if result:
                return result
        return self.checkDiagonals(temp_board)

    def is_tie(self):
        if '' in np.array(self.board):
            return False
        return True
