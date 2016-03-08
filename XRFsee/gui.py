import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
try:
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar2QT
except ImportError:
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT

from matplotlib.figure import Figure


# class myListWidget(QListWidget):
#     def __init__(self, parent = None):
#         super(myListWidget, self).__init__(parent)
#         #self.runID = ''
#
#     def Clicked(self,item):
#         self.runID = item
#         QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())
#
#     # def mousePressEvent(self, event):
#     #     # if event.button() == Qt.LeftButton:
#     #     #     print('Pressed')
#     #     if event.button() == Qt.RightButton:
#     #         print('Right button Pressed')

class RunIDWidget(QWidget):
    """
    A composite widget of ListWidget and load/del button.
    """
    def __init__(self, parent = None):
        super(RunIDWidget, self).__init__(parent)

        layout = QVBoxLayout()
        self.runid_list_w = QListWidget()
        load_del = QHBoxLayout()
        load_btn = QPushButton('Load')
        load_btn.clicked.connect(self.load_runid)
        del_btn = QPushButton('Delete')
        del_btn.clicked.connect(self.del_runid)
        load_del.addWidget(load_btn)
        load_del.addWidget(del_btn)
        layout.addWidget(self.runid_list_w)
        layout.addLayout(load_del)
        self.setLayout(layout)

    def load_runid(self):
        print('load runid {}'.format(self.runid_list_w.currentItem()))

    def del_runid(self):
        self.runid_list_w.takeItem(self.runid_list_w.currentRow())

    def addItem(self, item):
        out = self.runid_list_w.findItems(item, Qt.MatchFlag(0))

        if len(out) == 0:
            self.runid_list_w.addItem(item)
            self.runid_list_w.sortItems(order=Qt.AscendingOrder)


class RunIDList(QWidget):
    def __init__(self, parent = None):
        super(RunIDList, self).__init__(parent)
        self.runID = ''
        self.vbox = QVBoxLayout()
        self.namelist = []
        #self.button_list = []
        self.setLayout(self.vbox)

    def addItem(self, v):
        v = str(v)
        if v not in self.namelist:
            self.namelist.append(v)
            tmp_w = QWidget()
            tmp_l = QHBoxLayout()
            tmp_w.setLayout(tmp_l)

            button = QPushButton(v)
            button.clicked.connect(self.clicked)
            del_b = QPushButton('Delete')
            del_b.clicked.connect(self.clicked)
            #fbox = QFormLayout()
            #fbox.addRow(button, del_b)
            tmp_l.addWidget(button)
            tmp_l.addWidget(del_b)
            self.vbox.addWidget(tmp_w)

    def clicked(self,item):
        #self.runID = item.text()
        print(item)
        #QMessageBox.information(self, "ListWidget", "You clicked: "+item)


class MplCanvas(FigureCanvas):
    """
    Canvas which allows us to use matplotlib with pyqt4
    """
    def __init__(self, fig=None, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        # We want the axes cleared every time plot() is called
        self.axes = fig.add_subplot(1, 1, 1)
        self.axes.hold(False)

        FigureCanvas.__init__(self, fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._title = ''
        self.title_font = {'family': 'serif', 'fontsize': 10}
        self._title_size = 0
        self.figure.subplots_adjust(top=0.95, bottom=0.15)

        window_brush = self.window().palette().window()
        #fig.set_facecolor(brush_to_color_tuple(window_brush))
        #fig.set_edgecolor(brush_to_color_tuple(window_brush))
        self._active = False

    def _get_title(self):
        return self._title

    def _set_title(self, title):
        self._title = title
        if self.axes:
            self.axes.set_title(title, fontdict=self.title_font)
            # bbox = t.get_window_extent()
            # bbox = bbox.inverse_transformed(self.figure.transFigure)
            # self._title_size = bbox.height
            # self.figure.subplots_adjust(top=1.0 - self._title_size)

    title = property(_get_title, _set_title)


class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Demo: Control Engine for XRF Experiments')

        self.main_frame = QWidget()

        self.data_list = []
        self.all_pv = []

        # load data based on runID
        self.loaddata_frame = QFrame()
        runid_hbox = QHBoxLayout()
        run_num_l = QLabel()
        run_num_l.setText('Run ID')
        self.textbox = QLineEdit()
        self.textbox.setMinimumWidth(200)
        #self.connect(self.textbox, SIGNAL('editingFinished ()'), self.on_draw)
        runid_hbox.addWidget(run_num_l)
        runid_hbox.addWidget(self.textbox)

        load_button = QPushButton("Add")
        self.connect(load_button, SIGNAL('clicked()'), self.runid_frame)

        search_button = QPushButton("Search")

        load_vbox = QVBoxLayout()
        load_vbox.addLayout(runid_hbox)

        for w in [  load_button, search_button]:
            load_vbox.addWidget(w)
            #hbox.setAlignment(w, Qt.AlignVCenter)

        self.loaddata_frame.setLayout(load_vbox)

        # display data and pv list
        self.showdata_frame = QFrame()
        self.showdata_layout = QVBoxLayout()
        #self.runid_widget = myListWidget()
        #self.runid_widget = RunIDList()
        self.runid_widget = RunIDWidget()
        self.pv_widget = myListWidget()

        self.showdata_layout.addWidget(self.runid_widget)
        #self.runid_widget.itemClicked.connect(self.get_run_id)

        self.showdata_layout.addWidget(self.pv_widget)
        self.pv_widget.itemClicked.connect(self.pv_widget.Clicked)

        self.showdata_frame.setLayout(self.showdata_layout)

        #self.create_main_frame()

        #self.runid_frame()
        self.create_menu()
        #self.create_main_frame()
        #self.create_status_bar()

        # Plotting frame
        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        #self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = MplCanvas(width=6, height=4, dpi=self.dpi)
        #self.canvas = FigureCanvas(self.fig)
        #self.canvas.setParent(self.main_frame)

        # Since we have only one plot, we can use add_axes
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        #self.axes = self.fig.add_subplot(111)

        # Bind the 'pick' event for clicking on one of the bars
        #
        self.canvas.mpl_connect('pick_event', self.on_pick)

        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar2QT(self.canvas, self.main_frame)

        plot_frame = QFrame()
        plot_vbox = QVBoxLayout()
        plot_vbox.addWidget(self.mpl_toolbar)
        plot_vbox.addWidget(self.canvas)
        plot_frame.setLayout(plot_vbox)

        # Put all things together
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.loaddata_frame)
        splitter1.addWidget(self.showdata_frame)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(splitter1)
        splitter.addWidget(plot_frame)
        self.setCentralWidget(splitter)

    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"

        path = unicode(QFileDialog.getSaveFileName(self,
                        'Save file', '',
                        file_choices))
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def on_about(self):
        msg = """ A demo of using PyQt with matplotlib:

         * Use the matplotlib navigation bar
         * Add values to the text box and press Enter (or click "Draw")
         * Show or hide the grid
         * Drag the slider to modify the width of the bars
         * Save the plot to a file using the File menu
         * Click on a bar to receive an informative message
        """
        QMessageBox.about(self, "About the demo", msg.strip())

    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        #
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points

        QMessageBox.information(self, "Click!", msg)

    def on_draw(self):
        """ Redraws the figure
        """
        str = unicode(self.textbox.text())
        self.data = map(int, str.split())

        x = range(len(self.data))

        # clear the axes and redraw the plot anew
        #
        self.axes.clear()
        self.axes.grid(self.grid_cb.isChecked())

        self.axes.bar(
            left=x,
            height=self.data,
            width=self.slider.value() / 100.0,
            align='center',
            alpha=0.44,
            picker=5)

        self.canvas.draw()


    def runid_frame(self):
        """
        Add run number to a list and display.
        """
        #self.data_list.append(self.textbox.text())
        #print(self.data_list)

        #self.runid_widget.runid_list.clear()
        #self.runid_widget.runid_list.addItems(list(set(self.data_list)))
        self.runid_widget.addItem(self.textbox.text())
        #self.runid_widget.addItem(self.textbox.text())
        #self.create_main_frame()

    def get_run_id(self, runid):
        print('runid is {}'.format(runid.text()))
        self.pv_widget.clear()
        self.pv_widget.addItem(runid.text())

        #self.create_main_frame()

    # def create_main_frame(self):
    #     self.main_frame = QWidget()
    #
    #     # Create the mpl Figure and FigCanvas objects.
    #     # 5x4 inches, 100 dots-per-inch
    #     #
    #     self.dpi = 100
    #     self.fig = Figure((5.0, 4.0), dpi=self.dpi)
    #     self.canvas = FigureCanvas(self.fig)
    #     self.canvas.setParent(self.main_frame)
    #
    #     # Since we have only one plot, we can use add_axes
    #     # instead of add_subplot, but then the subplot
    #     # configuration tool in the navigation toolbar wouldn't
    #     # work.
    #     #
    #     self.axes = self.fig.add_subplot(111)
    #
    #     # Bind the 'pick' event for clicking on one of the bars
    #     #
    #     #self.canvas.mpl_connect('pick_event', self.on_pick)
    #
    #     # Create the navigation toolbar, tied to the canvas
    #     #
    #     self.mpl_toolbar = NavigationToolbar2QT(self.canvas, self.main_frame)
    #
    #     plot_frame = QFrame()
    #     vbox_plot = QVBoxLayout()
    #     vbox_plot.addWidget(self.canvas)
    #     vbox_plot.addWidget(self.mpl_toolbar)
    #     plot_frame.setLayout(vbox_plot)
    #
    #     splitter1 = QSplitter(Qt.Vertical)
    #     splitter1.addWidget(self.loaddata_frame)
    #     splitter1.addWidget(self.showdata_frame)
    #     #splitter1.addWidget(self.pv_frame)
    #
    #     splitter = QSplitter(Qt.Horizontal)
    #     splitter.addWidget(splitter1)
    #     splitter.addWidget(plot_frame)
    #
    #     #self.main_frame.setLayout(splitter2)
    #     #self.setCentralWidget(self.main_frame)
    #     self.setCentralWidget(splitter)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        load_file_action = self.create_action("&Save plot",
            shortcut="Ctrl+S", slot=self.save_plot,
            tip="Save the plot")
        quit_action = self.create_action("&Quit", slot=self.close,
            shortcut="Ctrl+Q", tip="Close the application")

        self.add_actions(self.file_menu,
            (load_file_action, None, quit_action))

        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About",
            shortcut='F1', slot=self.on_about,
            tip='About the demo')

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None,
                        icon=None, tip=None, checkable=False,
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
