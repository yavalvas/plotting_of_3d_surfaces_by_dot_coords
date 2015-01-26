#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import sys
from PyQt4 import QtCore

from PyQt4.QtGui import QMainWindow, \
    QFileDialog, QMessageBox, QWidget, QLineEdit, \
    QPushButton, QCheckBox, QComboBox, QHBoxLayout, \
    QTabWidget, QVBoxLayout, QLabel, QAction, \
    QIcon, QApplication, QTextCursor, QTextEdit
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
#from matplotlib.patches import Circle
#from matplotlib.lines import Line2D
from itertools import izip
# from joblib import delayed, Parallel
# import multiprocessing
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np
#from matplotlib import contour
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
from matplotlib import cm, rcParams

# class AgeSelector(QWidget):
#     def __init__(self, canvas, axes):
#         self.axes = axes
#         self.canvas2 = canvas
#         QWidget.__init__(self,*args)
#         self.setWindowTitle(u"Скорость, с которой движется линза [м/с]")
#         self.setLayout(layout)



class AppForm(QMainWindow):
    def __init__(self, parent=None):
        # try:
        #     self.cpus = multiprocessing.cpu_count()
        # except NotImplementedError:
        #     self.cpus = 2   # arbitrary default

        # sys.stdout = EmittedStream(textWritten=self.normalOutputWritten)
        # sys.stderr = EmittedStream(textWritten=self.normalOutputWritten)
        QMainWindow.__init__(self, parent)
        self.showMaximized()

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
        self.draw_results_1_7125()
        self.draw_results_2_417()

    def create_status_bar(self):
        self.status_text = QLabel(
            u"Расчет интерферометра.\nВычисление оптической разности хода лучей")
        self.statusBar().addWidget(self.status_text, 1)
    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
    def on_about(self):
        msg = u""" Приложение - результаты моделирования интерферометра
        Автор: Яворский Александр (yavalvas@gmail.com)
        Исходники: https://yavorskiy-av@bitbucket.org/yavorskiy-av/plotting_of_3d_surfaces_by_dot_coords
        """
        #Встраивание matplotlib в GUI повзаимствовано от Eli Bendersky (eliben@gmail.com)
        QMessageBox.about(self, u"О приложении 'Результаты матмоделирования иф-ра'", msg.strip())

    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"

        path = unicode(QFileDialog.getSaveFileName(self,
                                                   u'Сохранить файл', '',
                                                   file_choices))
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage(u'Сохранено в %s' % path, 2000)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu(u"&Файл")

        load_file_action = self.create_action(u"&Сохранить построение",
                                              shortcut="Ctrl+S", slot=self.save_plot,
                                              tip=u"Сохранить рисунок")
        quit_action = self.create_action(u"&Выйти", slot=self.close,
                                         shortcut="Ctrl+Q", tip="Close the application")

        self.add_actions(self.file_menu,
                         (load_file_action, None, quit_action))

        self.help_menu = self.menuBar().addMenu(u"&Помощь")
        about_action = self.create_action(u"&О приложении",
                                          shortcut='F1', slot=self.on_about,
                                          tip=u'О приложении')

        self.add_actions(self.help_menu, (about_action,))
    def draw_results_1_7125(self):
        self.axes.clear()
        X = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3,
             5e3, 5e3, 5e3, 5e3, 5e3, 5e3, 5e3, 5e3, 5e3, 5e3,
             1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4,
             1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4,
             2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4,
             2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4,
             3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4,
             5e4, 5e4, 5e4, 5e4, 5e4, 5e4, 5e4, 5e4, 5e4, 5e4,
             1e5, 1e5, 1e5, 1e5, 1e5, 1e5, 1e5, 1e5, 1e5, 1e5,
             1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5,
             2e5, 2e5, 2e5, 2e5, 2e5, 2e5, 2e5, 2e5, 2e5, 2e5,
             2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5,
             3e5, 3e5, 3e5, 3e5, 3e5, 3e5, 3e5, 3e5, 3e5, 3e5]
        Y = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
             0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818]
        Z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0.00000001359492565, 0.00000002745297888, 0.00000004139874132, 0.00000005516908536, 0.000000068764011, 0.0000000826220643, 0.0000000963046991, 0.0000001101627523, 0.0000001244593516,
             0, 0.00000006902713859, 0.0000001381419864, 0.0000002069937066, 0.0000002760208452, 0.0000003449602746, 0.0000004137242857, 0.0000004827514242, 0.000000551866272, 0.0000006222090486,
             0, 0.0000001381419864, 0.0000002761962636, 0.0000004140751224, 0.0000005521293996, 0.0000006900959675, 0.0000008280625355, 0.0000009661168127, 0.000001103907962, 0.000001244330388,
             0, 0.0000002066428698, 0.0000004139874132, 0.0000006209811198, 0.0000008279748264, 0.000001034880824, 0.000001241699112, 0.000001448605109, 0.000001655774234, 0.000001866100891,
             0, 0.0000002757577176, 0.0000005517785628, 0.0000008278871172, 0.000001103732544, 0.000001379577971, 0.000001655598816, 0.000001931619661, 0.000002207640506, 0.000002488046811,
             0, 0.0000003452234022, 0.0000006899205492, 0.000001034968533, 0.000001380016517, 0.000001724889082, 0.000002069937066, 0.000002414809631, 0.000002759857615, 0.000003110431278,
             0, 0.0000004139874132, 0.0000008278871172, 0.000001241699112, 0.000001655774234, 0.000002069849357, 0.000002483661351, 0.000002897648765, 0.000003311636178, 0.000003732201781,
             0, 0.00000068983284, 0.000001379841098, 0.000002069673938, 0.000002759769906, 0.000003449515037, 0.000004139698714, 0.000004829531554, 0.000005519364394, 0.00000622051172,
             0, 0.000001379841098, 0.000002759769906, 0.000004139611004, 0.000005519539812, 0.000006899205492, 0.000008279222009, 0.000009658975398, 0.00001103890421, 0.00001244146199,
             0, 0.000002069849357, 0.000004139698714, 0.00000620963578, 0.000008279397427, 0.00001034907137, 0.00001241900843, 0.00001448877008, 0.00001655844402, 0.00001866223683,
             0, 0.000002759682197, 0.000005519452103, 0.000008279309718, 0.00001103899191, 0.00001379876182, 0.00001655818089, 0.0000193180385, 0.00002207807154, 0.00002488266084,
             0, 0.000003449778164, 0.00000689946862, 0.00001034907137, 0.00001379867411, 0.0000172487154, 0.0000206978796, 0.00002414774548, 0.00002759743593, 0.00003110343569,
             0, 0.000004139523295, 0.00000827904659, 0.0000124187453, 0.00001655853173, 0.00002069796731, 0.00002483757832, 0.00002897710161, 0.00003311662491, 0.00003732412283]
        xi = np.linspace(np.min(X), np.max(X))
        yi = np.linspace(np.min(Y), np.max(Y))
        zi = griddata(X, Y, Z, xi, yi)
        plt.contour(xi, yi, zi)
        fig = plt.figure()
        self.axes.set_title(u"Без дисперсии с n1=1.7127, Umax = 45.0818 до beta=1E-3")
        self.axes.set_xlabel(u'Vo[м/с]')
        self.axes.set_ylabel(u'Vd[м/с]')
        self.axes.set_zlabel(u'ddle[ед]')
        zlabs = ['{:1.1E}'.format(i*1E-6) for i in xrange(0, 45, 5)]
        self.axes.set_zticklabels(zlabs)
        self.axes.set_zticks(zlabs)
        xlabs = ['{:1.1E}'.format(i) for i in xrange(0, 350000, 50000)]
        self.axes.set_xticklabels(xlabs)
        self.axes.set_xticks(xlabs)
        ylabs = ['{:1.0E}'.format(i*10) for i in xrange(0, 6, )]
        self.axes.set_yticklabels(ylabs)
        self.axes.set_yticks(ylabs)
        xim, yim = np.meshgrid(xi, yi)
        Gx, Gy = np.gradient(zi) #gradient with respect to x and y
        G = (Gx**2+Gy**2)**.5 #gradient magitude
        N = G/G.max()# normalize 0..1
        self.axes.plot_surface(xim, yim, zi, rstride=1, cstride=1, facecolors=cm.jet(N), linewidth=0, antialiased=False, shade=False)
        self.canvas.draw()

    def draw_results_2_417(self):
        self.axes1.clear()
        # self.axes.plot(list_x1_axis, list_y1_axis, c="r")
        X = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4,
             1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4,
             2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4,
             2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4,
             3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4,  3e4, 3e4, 3e4,
             5e4, 5e4, 5e4, 5e4, 5e4, 5e4, 5e4, 5e4, 5e4, 5e4, 5e4, 5e4, 5e4,
             1e5, 1e5, 1e5, 1e5, 1e5, 1e5, 1e5, 1e5, 1e5, 1e5, 1e5, 1e5, 1e5,
             1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5, 1.5e5,
             2e5, 2e5, 2e5, 2e5, 2e5, 2e5, 2e5, 2e5, 2e5, 2e5, 2e5, 2e5, 2e5,
             2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5, 2.5e5,
             3e5, 3e5, 3e5, 3e5, 3e5, 3e5, 3e5, 3e5, 3e5, 3e5, 3e5, 3e5, 3e5]
        Y = [0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119,
             0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119,
             0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119,
             0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119,
             0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119,
             0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119,
             0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119,
             0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119,
             0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119,
             0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119,
             0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119,
             0, 100, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5152.2119]
        Z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0.000004526408566, 0.00001357975195, 0.00002263335847, 0.00004526671694, 0.00006789981228, 0.0000851572986, 0.0000959176384, 0.0001066780659, 0.0001174384057, 0.0001281987455, 0.0001389589976, 0.0001529949251,
             0, 0.000006789919832, 0.0000203697595, 0.00003394994999, 0.00006789989999, 0.0001018494992, 0.0001357994491, 0.0001697487852, 0.0001915627643, 0.0002077034494, 0.000223843696, 0.0002399839425, 0.0002610376584,
             0, 0.000009053431097, 0.00002716003016, 0.00004526671694, 0.00009053334617, 0.0001357995368, 0.0001810658152, 0.0002263317428, 0.0002715978458, 0.0003168635102, 0.0003405197333, 0.000362039799, 0.0003901113908,
             0, 0.00001131667923, 0.0000339500377, 0.00005658357159, 0.0001131667046, 0.0001697498377, 0.0002263325322, 0.0002829150513, 0.0003394973072, 0.0003960793877, 0.0004526613806, 0.0005051269176, 0.0005402160347,
             0, 0.00001358010279, 0.00004074022066, 0.00006790007541, 0.0001357999754, 0.0002036996123, 0.0002715991614, 0.0003394979212, 0.0004073967687, 0.0004752952653, 0.0005431935865, 0.0006110913815, 0.0006996588137,
             0, 0.00002263344618, 0.00006790025083, 0.0001131667046, 0.0002263331461, 0.0003394991491, 0.0004526646258, 0.0005658297517, 0.0006789945267, 0.0007921584247, 0.0009053224103, 0.001018485782, 0.001166098081,
             0, 0.00004526680465, 0.0001358003262, 0.0002263335847, 0.0004526665554, 0.0006789984736, 0.0009053294271, 0.001131659591, 0.001357988966, 0.001584317726, 0.001810645171, 0.002036971827, 0.002332196601,
             0, 0.00006790025083, 0.0002037006648, 0.0003395006402, 0.0006789999647, 0.001018497798, 0.001357994404, 0.001697489957, 0.002036984282, 0.002376476677, 0.002715968283, 0.003055458399, 0.003498295384,
             0, 0.0000905336093, 0.0002716005648, 0.0004526676956, 0.000905333374, 0.001357997561, 0.001810659907, 0.002263320322, 0.002715979423, 0.003168636593, 0.003621291922, 0.004073945321, 0.004664395044,
             0, 0.0001131669678, 0.0003395013418, 0.0005658350142, 0.001131667134, 0.001697497324, 0.002263325497, 0.00282915139, 0.003394975265, 0.003960796597, 0.004526616174, 0.005092433559, 0.005830495581,
             0, 0.0001358005894, 0.0004074012418, 0.0006790018066, 0.001358001333, 0.002036997789, 0.002715991877, 0.003394983246, 0.004073971721, 0.004752957916, 0.005431941654, 0.006110922674, 0.006996597434]
        xi = np.linspace(np.min(X), np.max(X))
        yi = np.linspace(np.min(Y), np.max(Y))
        zi = griddata(X, Y, Z, xi, yi)
        plt.contour(xi, yi, zi)
        fig = plt.figure()
        #ax = Axes3D(fig)
        # ax = fig.add_subplot(111, projection='3d')
        self.axes1.set_title(u"Без дисперсии с n1=2.417, Umax = 5152.2119 до beta=1E-3")
        #ax.set_ylim(0,1)
        self.axes1.set_xlabel(u'Vo[м/с]')
        self.axes1.set_ylabel(u'Vd[м/с]')
        self.axes1.set_zlabel(u'ddle[ед]')
        zlabs = ['{:1.1E}'.format(i*1E-3) for i in xrange(0, 8, 1)]
        self.axes1.set_zticklabels(zlabs)
        self.axes1.set_zticks(zlabs)
        #xlabs = ['{:1.0E}'.format(i*1E2) for i in xrange(0, 350, 50)]
        xlabs = ['{:1.1E}'.format(i) for i in xrange(0, 350000, 50000)]
        self.axes1.set_xticklabels(xlabs)
        self.axes1.set_xticks(xlabs)
        ylabs = ['{:1.0E}'.format(i*1E3) for i in xrange(0, 7)]
        self.axes1.set_yticklabels(ylabs)
        self.axes1.set_yticks(ylabs)
        xim, yim = np.meshgrid(xi, yi)
        Gx, Gy = np.gradient(zi) #gradient with respect to x and y
        G = (Gx**2+Gy**2)**.5
         #gradient magitude
        N = G/G.max()# normalize 0..1
        self.axes1.plot_surface(xim, yim, zi, rstride=1, cstride=1, facecolors=cm.jet(N), linewidth=0, antialiased=False, shade=False)
        self.canvas1.draw()

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
    def create_action(self, text, slot=None, shortcut=None,
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
            self.connect(action, QtCore.SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
    def create_main_frame(self):
        self.main_frame = QWidget()
        self.main_frame1 = QWidget()
        self.dpi = 100
        self.fig = Figure((5.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.dpi1 = 100
        self.fig1 = Figure((5.0, 5.0), dpi=self.dpi1)
        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas1.setParent(self.main_frame1)
        self.axes = p3.Axes3D(self.fig)
        self.axes1 = p3.Axes3D(self.fig1)
        self.canvas.mpl_connect('pick_event', self.on_pick)
        self.canvas1.mpl_connect('pick_event', self.on_pick)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        self.mpl_toolbar1 = NavigationToolbar(self.canvas1, self.main_frame1)
        tab_widget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        vbox1 = QVBoxLayout(tab1)

        vbox1.addWidget(self.canvas)
        vbox1.addWidget(self.mpl_toolbar)

        vbox2 = QVBoxLayout(tab2)
        vbox2.addWidget(self.canvas1)
        vbox2.addWidget(self.mpl_toolbar1)

        tab_widget.addTab(tab1, u"n=1.7125(ТФ3)")
        tab_widget.addTab(tab2, u"n=2.417")

        vbox = QVBoxLayout()
        vbox.addWidget(tab_widget)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu(u"&Файл")

        load_file_action = self.create_action(u"&Сохранить построение",
                                              shortcut="Ctrl+S", slot=self.save_plot,
                                              tip=u"Сохранить рисунок")
        quit_action = self.create_action(u"&Выйти", slot=self.close,
                                         shortcut="Ctrl+Q", tip="Close the application")

        self.add_actions(self.file_menu,
                         (load_file_action, None, quit_action))

        self.help_menu = self.menuBar().addMenu(u"&Помощь")
        about_action = self.create_action(u"&О приложении",
                                          shortcut='F1', slot=self.on_about,
                                          tip=u'О приложении')

        self.add_actions(self.help_menu, (about_action,))
def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()