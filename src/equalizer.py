import time

import numpy as np

from PyQt5 import QtWidgets
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from scipy import signal
from controlers import Controlers
from audio_viewer import Viewer
from equalizer_worker import Equalizer_worker
from src.spectogram_viewer import Spectogram_viewer
import sounddevice as sd
import qtawesome as qta



def addIcon(name, icon, layout, color):
    icon = qta.IconWidget(icon, color=color)
    icon.setSizePolicy(qtw.QSizePolicy.Policy.Maximum,
                       qtw.QSizePolicy.Policy.Maximum)
    icon.setIconSize(qtc.QSize(32, 32))
    icon.setToolTip(name)
    icon.update()
    layout.addWidget(icon)

class Equalizer(QtWidgets.QWidget):
    slider_gain = qtc.pyqtSignal(object,float,tuple,float)

    def __init__(self):
        super().__init__()
        uic.loadUi("UI/equalizer.ui", self)
        self.FREQ_RANGE1=(60,200)
        self.FREQ_RANGE2 =(600,3000)
        self.FREQ_RANGE3 =(5000,10000)

        self.time=[]
        self.data=[]
        self.aux_data=[]
        self.sampling_rate=0
        self.viewer = Viewer()
        self.spectogram_viewer=Spectogram_viewer()

        self.player_layout.addWidget(self.viewer)
        self.spectogram_layout.addWidget(self.spectogram_viewer)
        self.init_icons()


        self.Start_button.clicked.connect(self.start_viewer)
        self.Stop_button.clicked.connect(self.stop)
        self.Volume_slider.sliderReleased.connect(self.change_volume)

        self.sliders_arr = [self.Drum_slider, self.Piano_slider, self.Piccolo_slider]
        self.signals_equalizing_arr = [lambda i=0,freq_range1=self.FREQ_RANGE1: self.threading(i,freq_range1),
                                          lambda i=1,freq_range2=self.FREQ_RANGE2: self.threading(i,freq_range2),
                                          lambda i=2,freq_range3=self.FREQ_RANGE3: self.threading(i,freq_range3)]

        for i in range(len(self.sliders_arr)):
            self.sliders_arr[i].sliderReleased.connect(self.signals_equalizing_arr[i])

        self.equalizer_thread = qtc.QThread()
        self.equalizer_Worker = Equalizer_worker()
        self.equalizer_Worker.moveToThread(self.equalizer_thread)
        self.equalizer_thread.start()

        self.slider_gain.connect(self.equalizer_Worker.equalize)
        self.equalizer_Worker.equalized.connect(self.update_data)


    def uiDesigner(self):
        self.sliders = {"Piano": ["mdi.piano", self.PianoIcon, "green"],
                        "Piccolo": ["ph.magic-wand-thin", self.PiccoloIcon, "red"],
                        "Snare": ["fa5s.drum", self.SnareIcon, "blue"],
                        "Speaker": ["ei.speaker", self.SpeakerIcon, "blue"]}

        for slider_name in self.sliders.keys():
            slider = self.sliders[slider_name]
            addIcon(slider_name, slider[0], slider[1], slider[2])

        self.Start_button.setIcon(self.style().standardIcon(
            qtw.QStyle.StandardPixmap.SP_MediaPlay))
        self.Stop_button.setIcon(self.style().standardIcon(
            qtw.QStyle.StandardPixmap.SP_MediaStop))


        pulse_icon = qta.icon('mdi6.replay')

        self.Raply_button.setIcon(pulse_icon)
        self.Raply_button.setIconSize(qtc.QSize(60, 17))




    def init_icons(self):
        self.uiDesigner()



    def loading_data(self,data,sampling_rate):

        self.data=data[:,0]
        self.aux_data = self.data.copy()
        # print((sampling_rate))

        self.sampling_rate = sampling_rate
        duration = len(self.data)/self.sampling_rate
        self.time= np.linspace(0,duration,len(self.data))

        # print(sampling_rate)
        self.viewer.load_data(self.time, self.aux_data,sampling_rate)




    def start_viewer(self):
        # print("sssssssssssss")
        # print(self.sampling_rate)
        self.spectogram_viewer.draw_spectogram(self.aux_data)
        # data = self.data*2.0 ** 15
        # print(self.data)/
        # sd.play(self.data, self.sampling_rate )
        self.viewer.start()

    def stop(self):
        self.viewer.stop_viewer()



    def threading(self,i,freq_range):
        gain = self.sliders_arr[i].value()
        self.slider_gain.emit(self.aux_data, gain, freq_range, self.sampling_rate)


    # def move_to_equalizer(self,i,freq_range):
    #     gain =self.sliders_arr[i].value()
    #     #
    #     # print(self.data)
    #     # print(gain)
    #     # print(freq_range)
    #     # print(self.sampling_rate)
    #
    #     self.equalize(self.data,gain,freq_range,self.sampling_rate)
    #     # print(gain)
    #
    # def equalize(self,data,gain,freq_range,sampling_freq):
    #     if (gain/100)>=0.5:
    #         gain = gain/100 + 1
    #
    #     elif (gain/100)<0.5 and (gain/100)>0 :
    #         gain = gain / 100 + 0.5
    #
    #     elif(gain/100) == 0:
    #         gain = 0
    #     # gain=gain/100
    #
    #     # data = data / 2.0 ** 15
    #     amp = np.fft.rfft(data)
    #
    #     # amp_equalized = amp.copy()  ###### if you want to plot the change befor equalizing (amp) and after (amp_equalized)
    #     freq = np.fft.rfftfreq(len(data), 1 / sampling_freq)
    #
    #     for i, f in enumerate(freq):
    #
    #         if f > freq_range[0] and f < freq_range[1]:  # (1)
    #             amp[i] = amp[i] * gain
    #
    #     data_after_change = np.fft.irfft(amp)
    #     # print(data_after_change)

        # self.update_data(data_after_change)

    def change_volume(self):
        self.aux_data = self.data.copy()
        value = self.Volume_slider.value()
        if value == self.Volume_slider.minimum():
            value=-50
        self.aux_data *= 1.3 ** value
        self.update_data(self.aux_data)

    def update_data(self, data):
        self.aux_data= data
        # print("data_after_change",data)
        self.viewer.update_data_eq(data)
        self.spectogram_viewer.update_data_eq(data)
