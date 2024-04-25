import sys

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from functools import partial

from logic import TicTacToe


class StartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()

    def _initUI(self):
        # Setting up text, ip input window, and button
        self.label = QLabel('Write a ip of server', self)
        self.ip_input = QLineEdit(self)
        self.apply_ip = QPushButton('Apply ip', self)

        # ip regexp
        reg_ex = QRegExp(
            r"^(?:1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])"
            r"(?:\.(?:1?[0-9]{1,2}|2[0-4][0-9]|25[0-5]))"
            r"{3}(?::(?:[0-9]{1,4}|[1-5][0-9]{4}|6[0-4]"
            r"[0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]))?$")
        self.ip_validator = QRegExpValidator(reg_ex, self.ip_input)
        self.ip_input.setValidator(self.ip_validator)

        #

        # Center it
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.ip_input)
        self.layout.addWidget(self.apply_ip)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        # Set size of window
        self.setGeometry(0, 0, 200, 200)
        self.show()

    def read_ip_on_click(self):
        potential_ip = self.ip_input.text()


class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._initUI()

    def click_event(self, btn:QPushButton, index:tuple):
        # Change the button
        letter = self.logic.get_place(index[0], index[1])
        font = QFont()
        font.setPointSize(50)
        btn.setFont(font)
        btn.setText(letter)
        btn.setDisabled(True)
        # Check if the game is ended
        if self.logic.is_win():
            sys.exit()


    def _initUI(self):
        #Seting up logic class
        self.logic = TicTacToe()

        # Making list of buttons
        self.positions_list = [[QPushButton(self), QPushButton(self), QPushButton(self)],
                               [QPushButton(self), QPushButton(self), QPushButton(self)],
                               [QPushButton(self), QPushButton(self), QPushButton(self)]]

        # Creating layout
        self.layout = QVBoxLayout(self)

        # Set name of opponent
        self.opponent_name = QLabel('Your opponent: "Weirdo"')
        self.opponent_name.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('QLabel{font-size: 10pt;}')
        self.layout.addWidget(self.opponent_name)

        # Adding buttons
        for row in self.positions_list:
            sub_layout = QHBoxLayout()
            for position in row:
                position.setFixedSize(100, 100)
                position.clicked.connect(partial(self.click_event, position, (self.positions_list.index(row), row.index(position))))
                sub_layout.addWidget(position)
            self.layout.addLayout(sub_layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        # Set size of window
        self.setGeometry(0, 0, 200, 200)
        self.show()
