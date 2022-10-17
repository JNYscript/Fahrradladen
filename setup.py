import sys

sys.path.insert(0,".\\objects")
sys.path.insert(0,".\\gui")
sys.path.insert(0,".\\objects\\viewports")

from PyQt5.QtWidgets import QApplication

from gui.functional_gui import MainWindow
from objects.klassen import *


def main():
    session = Session()
    app = QApplication(sys.argv)
    app.setStyleSheet("QToolTip { color: #aaaacc; background-color: #000000; border: 0px; }")

    main_win = MainWindow(session)
    main_win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()