import sys

from PyQt5.QtWidgets import QApplication

from view import ChooseWidget, GameWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start = ChooseWidget()
    sys.exit(app.exec_())
