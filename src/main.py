import sys

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic
import qdarkstyle
import sounddevice as sd

from src.equalizer import Equalizer
from tab_viewer import Tab_viewer
import audio_worker

class MainWindow(qtw.QMainWindow):
    """The main application window"""
    loaded_data = qtc.pyqtSignal(tuple)
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/Main.ui", self)
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.tab_viewer = Tab_viewer()

        self.ceteral_widgit = self.centralWidget().layout()
        self.ceteral_widgit.addWidget(self.tab_viewer)
        self.Open_file_action.triggered.connect(self.Load_csv_file)

    def Load_csv_file(self):
        self.sampling_rate ,self.data = audio_worker.Load_csv_file(self)
        print(self.sampling_rate)
        # sd.play(self.data[:,0], self.sampling_rate)
        data =self.data / 2.0 ** 15
        self.tab_viewer.Equalizer.loading_data(data,self.sampling_rate )
        # print(self.data[:,0])



def main():
    app = qtw.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()