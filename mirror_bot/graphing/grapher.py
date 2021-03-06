from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg

import collections
import random
import time
import math
import numpy as np


class dataQueue():
    def __init__(self, bufsize):
        self.leader = collections.deque([0.0]*bufsize, bufsize)
        self.follower = collections.deque([0.0]*bufsize, bufsize)


class axisData():
    def __init__(self, axis, bufsize):
        self.title = axis
        self.pos = dataQueue(bufsize)
        self.vel = dataQueue(bufsize)


class Grapher():

    def __init__(self, sampleinterval=0.1, timewindow=10., datafeed=None, size=(1920, 1080)):
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        self.databuffer = self.initData(self._bufsize)
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.datafeed = datafeed
        # PyQtGraph stuff
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title="Mirror Bot Plots")
        self.win.resize(*size)
        self.curves = self.initQtApp(self.win)
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.updatePlots)
        self.timer.start(self._interval)
        return

    def initData(self, bufsize):
        databuffer = [axisData('0', bufsize),
                      axisData('1', bufsize),
                      axisData('2', bufsize)]
        return databuffer

    def initQtApp(self, win):
        curves = {'0': {'pos': {'leader': None, 'follower': None}, 'vel': {'leader': None, 'follower': None}},
                  '1': {'pos': {'leader': None, 'follower': None}, 'vel': {'leader': None, 'follower': None}},
                  '2': {'pos': {'leader': None, 'follower': None}, 'vel': {'leader': None, 'follower': None}}}
        for d in self.databuffer:
            # position
            p = win.addPlot(title='Position ' + d.title)
            curves[d.title]['pos']['leader'] = p.plot(
                self.x, list(d.pos.leader), pen=(255, 0, 0))
            curves[d.title]['pos']['follower'] = p.plot(
                self.x, list(d.pos.follower), pen=(0, 255, 0))
            p.setYRange(-2, 2, padding=0)
            # velocity
            p = win.addPlot(title='Velocity ' + d.title)
            curves[d.title]['vel']['leader'] = p.plot(
                self.x, list(d.vel.leader), pen=(255, 0, 0))
            curves[d.title]['vel']['follower'] = p.plot(
                self.x, list(d.vel.follower), pen=(0, 255, 0))
            p.setYRange(-10, 10, padding=0)
            win.nextRow()
        return curves

    def randData(self):
        frequency = 0.5
        noise = random.normalvariate(0., 1.)
        new = 10.*math.sin(time.time()*frequency*2*math.pi) + noise
        return new

    def updateData(self):
        databuffer = self.databuffer
        if self.datafeed is None:
            for d in databuffer:
                # position
                d.pos.leader.append(self.randData())
                d.pos.follower.append(self.randData())
                # velocity
                d.vel.leader.append(self.randData())
                d.vel.follower.append(self.randData())
        else:
            for i, d in enumerate(databuffer):
                # position
                d.pos.leader.append(self.datafeed['leader_pos'][i])
                d.pos.follower.append(self.datafeed['follower_pos'][i])
                # velocity
                d.vel.leader.append(self.datafeed['leader_vel'][i])
                d.vel.follower.append(self.datafeed['follower_vel'][i])
        return

    def updatePlots(self):
        self.updateData()

        for d in self.databuffer:
            # position
            self.curves[d.title]['pos']['leader'].setData(
                self.x, list(d.pos.leader))
            self.curves[d.title]['pos']['follower'].setData(
                self.x, list(d.pos.follower))
            # velocity
            self.curves[d.title]['vel']['leader'].setData(
                self.x, list(d.vel.leader))
            self.curves[d.title]['vel']['follower'].setData(
                self.x, list(d.vel.follower))
        return

    def run(self):
        QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
    m = Grapher(sampleinterval=0.1, timewindow=10.)
    m.run()
