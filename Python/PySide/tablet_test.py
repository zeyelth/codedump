# -*- coding: utf-8 -*-
'''
Copyright (c) 2013 Victor Wåhlström

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.

   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.

   3. This notice may not be removed or altered from any source
   distribution.
'''


from PySide import QtGui, QtCore
import sys


class TabletTest(QtGui.QMainWindow):
    def __init__(self):
        super(TabletTest, self).__init__()
        self.resize(250, 250)
        self._pos = QtCore.QPoint(0, 0)
        self._pressure = 0
        self._tilt = QtCore.QSize(0, 0)
        self._erase = False

    def tabletEvent(self, event):
        self._pressure = event.pressure()
        self._pos = event.pos()
        self._erase = event.pointerType() == event.Eraser
        self._tilt = QtCore.QSize(event.xTilt(), event.yTilt())

        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.save()
        rect = self.rect()
        painter.setClipRect(rect)

        pen_rect = QtCore.QRect(self._pos, self._tilt)

        painter.fillRect(rect, QtGui.QColor(255, 255, 255))
        pen_color = QtGui.QColor(255, 0, 0) if self._erase else QtGui.QColor(0, 0, 0)
        pen_color.setAlphaF(self._pressure)
        painter.fillRect(pen_rect, pen_color)

        painter.restore()


def main():
    app = QtGui.QApplication(sys.argv)
    widget = TabletTest()
    widget.show()
    app.exec_()

if __name__ == '__main__':
    main()
