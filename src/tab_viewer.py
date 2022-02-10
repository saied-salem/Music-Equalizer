from PyQt5 import QtWidgets
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from equalizer import Equalizer as eq
class Tab_viewer(QtWidgets.QTabWidget):
    """The main application window"""

    def __init__(self):
        super().__init__()
        uic.loadUi("src/UI/Tab_viewer.ui", self)
        Equalizer = eq()

        self.Equalizer_layout.addWidget(Equalizer)
        # self.Sampler_layout.addWidget(self.sampler)
        # self.setCurrentWidget(self.sampler_tab)