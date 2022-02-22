import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc



class Equalizer_worker(qtc.QObject):

    equalized = qtc.pyqtSignal(object)

    @qtc.pyqtSlot(object,float,tuple,float)
    def equalize(self,data,gain,freq_range,sampling_freq):
        # if (gain/100)>=0.5:
        #     gain = gain/100 + 1
        #
        # elif (gain/100)<0.5 and (gain/100)>0 :
        #     gain = gain / 100 + 0.5
        #
        # elif(gain/100) == 0:
        #     gain = 0

        amp = np.fft.rfft(data)

        # amp_equalized = amp.copy()  ###### if you want to plot the change befor equalizing (amp) and after (amp_equalized)
        freq = np.fft.rfftfreq(len(data), 1 / sampling_freq)

        for i, f in enumerate(freq):

            if f > freq_range[0] and f < freq_range[1]:  # (1)
                amp[i] *= 1.15**gain

        data_after_change = np.fft.irfft(amp)
        # print(data_after_change)
        self.equalized.emit(data_after_change)

