import numpy as np

from PyQt5 import QtWidgets
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
from scipy import signal
from controlers import Controlers

class Equalizer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/UI/Equalizer_tab.ui", self)

        controlers = Controlers()
        self.controlers_layout.addWidget(controlers)

