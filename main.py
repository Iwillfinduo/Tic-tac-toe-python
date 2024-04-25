import sys

from PyQt5.QtWidgets import QApplication

from view import StartWidget, GameWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWidget = GameWidget()
    sys.exit(app.exec_())
