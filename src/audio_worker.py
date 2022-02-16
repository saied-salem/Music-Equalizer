import numpy as np
from PyQt5.QtWidgets import QFileDialog
from scipy.io import wavfile


def Load_csv_file(widget):

    fileName, b = QFileDialog.getOpenFileName(widget, "Choose File", "", "wav (*.wav)")
    # print(fileName)
    samplerate, data =  wavfile.read(fileName)

    return samplerate,data

def open_wav_file(path):

    samplerate, data = wavfile.read(path)
    # print(data)
    return samplerate,data

# samplerate, data = wavfile.read("file_example_WAV_2MG.wav")
# duration = len(data[:,0])/samplerate
# print(duration)
# time = np.linspace(0,duration,len(data[:,0]))
# chuncks = np.array_split(data[:,0],(time[-1]))
# t_chuncks = np.array_split(time,(time[-1]))
#
#
# print(samplerate)
# print(len(chuncks[0]))
# print(len(t_chuncks[0]))
#
#
# print(len(time)==len(data[:,0]))