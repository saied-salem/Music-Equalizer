from PyQt5 import QtCore as qtc
import numpy as np
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sounddevice as sd


class Viewer(PlotWidget):
    def __init__(self):
        super(Viewer, self).__init__()
        self.pen = pg.mkPen(color=(255, 0, 0))
        self.data_chuncks = []
        self.time_chuncks = None
        self.data = []
        self.time = []

        self.fs = 0
        self.i = 0
        self.graph = self.plot([], [], pen=self.pen)

    def load_data(self, time, data, fs):

        # print(data)
        self.fs = fs
        print(self.fs)
        self.data = np.int32(data)
        self.time = time
        # self.data_chuncks =
        self.time_chuncks = np.array_split(self.time, time[-1]*10)
        self.data_chuncks = np.array_split(self.data, time[-1]*10)
        # print(self.time_chunck)
        self.setYRange(min(np.int32(self.data)), max(np.int32(self.data)))

        # self.plot(data)

    def start(self):
        # print("vvvvvvv")
        self.i = 0

        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.updata_graph)
        # print(self.fs)
        # sd.play(self.data, self.fs, blocking=False)
        self.timer.start(90)

    def updata_graph(self):
        # print(self.time_chuncks)

        # print(time_chuncks)
        if self.i==int(self.time[-1]*10):
            self.timer.stop()
        else:
            # self.graph.setData(self.time_chuncks[self.i], self.data_chuncks[self.i])
            self.graph.setData( self.data[self.i*(self.fs//10) : (1+self.i)*(self.fs//10)])

            self.i += 1
        # print(self.i)
