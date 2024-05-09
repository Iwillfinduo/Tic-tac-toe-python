import json
import threading
import time
from functools import partial

from PyQt5.QtCore import Qt, QRegExp, QThread, pyqtSignal
from PyQt5.QtGui import QRegExpValidator, QFont, QMovie
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

from client import HostingClient, Connection
from logic import TicTacToe


class ChooseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def ClickOnConnect(self):
        self.connect = ConnectWidget()
        self.close()

    def ClickOnHost(self):
        self.host = HostWidget()
        self.close()

    def initUI(self):
        self.setWindowTitle('Choose your role')

        # Setting up buttons
        self.host_button = QPushButton('Host')
        self.host_button.clicked.connect(self.ClickOnHost)
        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.ClickOnConnect)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.host_button)
        self.layout.addWidget(self.connect_button)

        # Set size of window
        self.setGeometry(0, 0, 200, 200)
        self.show()


class HostWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ip = '127.0.0.1'
        self.port = 8080
        self.host = HostingClient(self.ip, self.port)
        self.initUI()
        self.thread = ConnectAwaiterThread(self)
        self.thread.finished.connect(self.thread_finished)
        self.thread.start()

    def thread_finished(self):
        print('Connected in widget')
        self.host.connection.send(json.dumps({'name': self.text.text()}).encode('utf-8'))
        while self.host.name is None:
            continue
        print(json.dumps({'name': self.text.text()}).encode('utf-8'))
        print(self.host.name)
        GameWidget(self.host.name, self.host)
        self.close()
    def initUI(self):
        self.setWindowTitle('Host')

        self.label = QLabel(f"Your IP is: {self.ip}:{self.port}")
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.another_label = QLabel('Awaiting connection...')
        self.another_another_label = QLabel('Insert your name')
        self.text = QLineEdit()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.another_label)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.another_another_label)
        self.layout.setAlignment(Qt.AlignCenter)

        # Set size of window
        self.setGeometry(0, 0, 200, 200)
        self.show()

class ConnectAwaiterThread(QThread):
    def __init__(self, main_widget : HostWidget):
        super().__init__()
        self.main_widget = main_widget

    def run(self):
        while not self.main_widget.host.is_connected:
            continue

        self.quit()

class ConnectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._initUI()

    def _initUI(self):
        # Setting up text, ip input window, and button
        self.ip_label = QLabel('Write a ip of server', self)
        self.ip_input = QLineEdit(self)
        self.name_label = QLabel('Write a name of a player', self)
        self.name_input = QLineEdit(self)
        self.apply_ip = QPushButton('Apply ip', self)
        self.apply_ip.clicked.connect(self.read_ip_on_click)

        # ip regexp
        reg_ex = QRegExp(
            r"^(?:1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])"
            r"(?:\.(?:1?[0-9]{1,2}|2[0-4][0-9]|25[0-5]))"
            r"{3}(?::(?:[0-9]{1,4}|[1-5][0-9]{4}|6[0-4]"
            r"[0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]))?$")
        self.ip_validator = QRegExpValidator(reg_ex, self.ip_input)
        self.ip_input.setValidator(self.ip_validator)

        # Center it
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.ip_input)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.apply_ip)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        # Set size of window
        self.setGeometry(0, 0, 200, 200)
        self.show()

    def read_ip_on_click(self):
        self.potential_ip = self.ip_input.text()
        self.nickname = self.name_input.text()
        client = Connection(self.potential_ip, self.nickname)
        while client.name is None:
            continue
        client.server_socket.send(json.dumps({'name': self.nickname}).encode('utf-8'))
        print(json.dumps({'name': self.nickname}).encode('utf-8'))
        GameWidget(client.name, client)
        self.close()


class GameWidget(QWidget):
    def __init__(self, name, host):

        super().__init__()

        self.logic = TicTacToe(host)


        self._initUI(name)
        print('out_initUI')
        self.opponent_thread = UpdateFromServer(self)
        self.opponent_thread.start()

    def click_event(self, btn: QPushButton, index: tuple):
        # Change the button
        letter = self.logic.get_place(index[0], index[1])
        if letter is not None:
            font = QFont()
            font.setPointSize(50)
            btn.setFont(font)
            btn.setText(letter)
            btn.setDisabled(True)

            # Check if the game is ended
            if self.logic.is_win() or self.logic.is_tie():
                self.close()

    def _initUI(self, name):
        # Setting up logic class

        # Making list of buttons
        self.positions_list = [[QPushButton(self), QPushButton(self), QPushButton(self)],
                               [QPushButton(self), QPushButton(self), QPushButton(self)],
                               [QPushButton(self), QPushButton(self), QPushButton(self)]]
        print('game is initing ui')
        # Creating layout
        self.layout = QVBoxLayout(self)
        # Set name of opponent
        self.opponent_name = QLabel(f'Your opponent: "{name}"\n You are {'X'if self.logic.is_you_cross else 'O'}')
        print(f'Your opponent: "{name}"')
        self.opponent_name.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('QLabel{font-size: 10pt;}')
        self.layout.addWidget(self.opponent_name)
        print('adding buttons')
        # Adding buttons
        for row in self.positions_list:
            sub_layout = QHBoxLayout()
            for position in row:
                position.setFixedSize(100, 100)
                position.clicked.connect(
                    partial(self.click_event, position, (self.positions_list.index(row), row.index(position))))
                sub_layout.addWidget(position)
            self.layout.addLayout(sub_layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)
        print('setting geometry')
        # Set size of window
        self.setGeometry(0, 0, 200, 200)
        print('after geometry')
        self.show()
        print('after show')


class UpdateFromServer(QThread):
    def __init__(self, mainwidget: GameWidget):
        print('init qthread')
        super().__init__()
        self.mainwidget = mainwidget
        self.logic = self.mainwidget.logic

    def run(self):
        print("I'm in qthread")
        while True:

            data = self.logic.get_update()
            if data is not None:
                target_button = self.mainwidget.positions_list[data['row']][data['col']]
                font = QFont()
                font.setPointSize(50)
                target_button.setFont(font)
                target_button.setText(data['letter'])
                target_button.setDisabled(True)

                # Check if the game is ended
                if self.logic.is_win() or self.logic.is_tie():
                    self.mainwidget.close()
