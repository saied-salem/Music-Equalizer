import matplotlib as matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as navigation_toolbar
from matplotlib.figure import Figure
plt.style.use('dark_background')
matplotlib.use('Qt5Agg')


class Spectogram_viewer(FigureCanvas):

    def __init__(self, parent=None, width=0.1, height=0.01, dpi=100):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        for spine in ['right', 'top', 'left', 'bottom']:
            self.axes.spines[spine].set_color('gray')
        # self.axes.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        super().__init__(self.fig)
        self.fig.tight_layout()
        self.axes.axis('off')
        self.cmap = plt.get_cmap('inferno')

    def draw_spectogram(self,data):
        self.axes.specgram(data, cmap=self.cmap)
        self.draw()

    def update_data_eq(self, data):
        self.axes.specgram(data , cmap=self.cmap)
        self.draw()


    def clear_canvans(self):
        self.axes.clear()
        self.draw()