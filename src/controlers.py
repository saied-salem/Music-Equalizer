import numpy as np

from PyQt5 import QtWidgets
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
from scipy import signal


class Controlers(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/UI/Controlers.ui", self)


