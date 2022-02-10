import sys

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic
import qdarkstyle

from tab_viewer import Tab_viewer


class MainWindow(qtw.QMainWindow):
    """The main application window"""

    def __init__(self):
        super().__init__()
        uic.loadUi("src/UI/Main.ui", self)
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.tab_viewer = Tab_viewer()
        self.ceteral_widgit = self.centralWidget().layout()
        self.ceteral_widgit.addWidget(self.tab_viewer)



def main():
    app = qtw.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()