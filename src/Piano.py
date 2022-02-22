from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
import sys
from PyQt5 import QtMultimedia
BlackIdx = 1, 3, -1, 6, 8, 10
WhiteIdx = 0, 2, 4, 5, 7, 9, 11
KeyNames = 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'

tones = ["wav/c.wav", "wav/c#.wav", "wav/d.wav", "wav/d#.wav",
         "wav/e.wav", "wav/f.wav", "wav/f#.wav",
         "wav/g.wav", "wav/g#.wav", "wav/A.wav", "wav/a#.wav", "wav/g#.wav"]


class KeyButton(qtw.QPushButton):
    triggered = qtc.pyqtSignal(int, bool)

    def __init__(self, key, isBlack=False):
        super().__init__()
        self.key = key
        # this will be used by the stylesheet
        self.setProperty('isBlack', isBlack)

        octave, keyIdx = divmod(key, 12)
        self.setText('{}{}'.format(KeyNames[keyIdx], octave))

        self.setMinimumWidth(25)
        self.setMinimumSize(25, 80 if isBlack else 120)

        # ensure that the key expands vertically
        self.setSizePolicy(qtw.QSizePolicy.Preferred,
                           qtw.QSizePolicy.Expanding)

        # connect the pressed and released (not clicked!) signals to our custom one
        self.pressed.connect(lambda: self.triggered.emit(key, True))
        # self.released.connect(lambda: self.triggered.emit(key, False))


class Keyboard(qtw.QWidget):
    def __init__(self, octaves=2, octaveStart=3):
        super().__init__()
        layout = qtw.QGridLayout(self)

        # the ratio between key heights: white keys are 1/3 longer than black ones
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 1)
        layout.setSpacing(0)

        blackKeys = []
        for octave in range(octaves):
            for k in range(12):
                isBlack = k in BlackIdx
                keyButton = KeyButton(k + (octaveStart + octave) * 12, isBlack)
                keyButton.triggered.connect(self.keyTriggered)
                if isBlack:
                    keyPos = BlackIdx.index(k)
                    # column based on the index of the key list, plus 2 "cells"
                    col = keyPos * 3 + 2
                    # only one row in the layout
                    vSpan = 1
                    # only two columns
                    hSpan = 2
                    blackKeys.append(keyButton)
                else:
                    keyPos = WhiteIdx.index(k)
                    col = keyPos * 3
                    # two rows
                    vSpan = 2
                    # three columns
                    hSpan = 3
                col += octave * 21
                layout.addWidget(keyButton, 0, col, vSpan, hSpan)

            # "blank" spacers between E-F and B-C, to keep the spacings homogeneous
            efSpacer = qtw.QWidget()
            efSpacer.setMinimumWidth(25)
            layout.addWidget(efSpacer, 0, octave * 21 + 8, 1, 2)
            efSpacer.lower()
            baSpacer = qtw.QWidget()
            baSpacer.setMinimumWidth(25)
            layout.addWidget(baSpacer, 0, octave * 21 + 20, 1, 2)
            baSpacer.lower()

        # the last C note, with a minimum width a bit bigger
        octave += 1
        lastButton = KeyButton((octaveStart + octave) * 12)
        lastButton.setMinimumWidth(32)
        lastButton.triggered.connect(self.keyTriggered)
        layout.addWidget(lastButton, 0, octave * 21, 2, 3)

        # raise all black keys on top of everything else
        for keyButton in blackKeys:
            keyButton.raise_()

        # set the stretch of layout cells, if it's in the middle, it's bigger
        for col in range(layout.columnCount()):
            if col % 3 == 1:
                layout.setColumnStretch(col, 4)
            else:
                layout.setColumnStretch(col, 3)

        self.setStyleSheet('''
            KeyButton {
                color: rgb(50, 50, 50);
                border: 1px outset rgb(128, 128, 128);
                border-radius: 2px;
                background: white;
            }
            KeyButton:pressed {
                border-style: inset;
            }
            KeyButton[isBlack=true] {
                color: rgb(250, 250, 250);
                background: black;
            }
            KeyButton[isBlack=true]:pressed {
                background: rgb(50, 50, 50);
            }
        ''')

    def keyTriggered(self, key, pressed):
        octave, keyIdx = divmod(key, 12)
        keyName = '{}{}'.format(KeyNames[keyIdx], octave)

        state = 'pressed' if pressed else 'released'

        sound_file = 'a3.wav'
        self.sound = QtMultimedia.QSound(tones[keyIdx])
        self.sound.play()

        # url = qtc.QUrl.fromLocalFile("a3.wav")
        # content = QtMultimedia.QMediaContent(url)
        # player = QtMultimedia.QMediaPlayer()
        # player.setMedia(content)
        # player.setVolume(50.0)
        # player.play()
        # playsound("a3.wav")
        print('Key {} ({}) {}'.format(key, keyName, state))


# if __name__ == '__main__':
#     import sys
#     app = qtw.QApplication(sys.argv)
#     keyboard = Keyboard()
#     keyboard.show()
#     sys.exit(app.exec_())
