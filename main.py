# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication
from NewMainWindow import *

import sys


def RunApplication():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    RunApplication()
