from PyQt5 import QtWidgets
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from equalizer import Equalizer as eq
from src.virtual_instrument import VirtualInstruments


class Tab_viewer(QtWidgets.QTabWidget):
    """The main application window"""

    def __init__(self):
        super().__init__()
        uic.loadUi("UI/Tab_viewer.ui", self)
        self.Equalizer = eq()

        self.instruments = VirtualInstruments()
        self.Virtual_instruments_layout.addWidget(self.instruments)

        self.Equalizer_layout.addWidget(self.Equalizer)

        self.setCurrentWidget(self.Equalizer_tab)


        # self.Sampler_layout.addWidget(self.sampler)
        # self.setCurrentWidget(self.sampler_tab)