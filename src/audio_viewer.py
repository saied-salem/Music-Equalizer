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
        self.hideAxis('bottom')
        # self.hideAxis('left')

    def load_data(self, time, data, fs):

        # print(data)
        self.i = 0
        self.fs = fs
        # print(self.fs)
        # self.data = np.int32(data)
        self.data =data
        self.time = time
        # self.data_chuncks =
        # self.time_chuncks = np.array_split(self.time, time[-1]*10)
        # self.data_chuncks = np.array_split(self.data, time[-1]*10)
        # print(self.time_chunck)
        self.setYRange(min((self.data))*2, max((self.data))*2)
        self.i=0

        # self.plot(data)

    def start(self):
        # print("start data",self.fs)
        # sd.stop()
        sd.play(self.data[(self.i)*(self.fs//10):], self.fs )

        self.start_viewer()
        # sd.play(self.data.tolist(), self.fs, blocking=False)


        # print(self.fs)
        data = self.data
        # print(self.fs)
        # print(data)

    def start_viewer(self):


        self.timer = qtc.QTimer()

        self.timer.timeout.connect(self.updata_graph)


        # sd.play(data, self.fs, blocking=True)
        self.timer.start(90)



    def updata_graph(self):
        # print(self.time_chuncks)

        # print("inside updaaatttaaa")
        if self.i==int(self.time[-1]*10):
            self.timer.stop()
        else:
            # self.graph.setData(self.time_chuncks[self.i], self.data_chuncks[self.i])
            self.graph.setData( self.data[self.i*(self.fs//10) : (1+self.i)*(self.fs//10)])

            self.i += 1
        # print(self.i)

    def stop_viewer(self):
        self.timer.stop()
        sd.stop()

    def update_data_eq(self,data):
        self.data = data
        # print("counter",self.i)
        sd.play(data[(self.i)*(self.fs//10):], self.fs)
