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

class OsdNotification(QtGui.QWidget):
    '''
    Provides a non-interactive popup widget for displaying informative text
    '''

    POSITION_TOP_LEFT = 0
    POSITION_TOP_RIGHT = 1
    POSITION_TOP_CENTER = 2
    POSITION_CENTER_LEFT = 3
    POSITION_CENTER_CENTER = 4
    POSITION_CENTER_RIGHT = 5
    POSITION_BOTTOM_LEFT = 6
    POSITION_BOTTOM_CENTER = 7
    POSITION_BOTTOM_RIGHT = 8

    def __init__(self, parent=None):
        super(OsdNotification, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool |
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._pos = self.POSITION_TOP_CENTER
        self._owner = None

        self._ttl_timer = QtCore.QTimer()
        self._ttl_timer.setSingleShot(True)
        self._ttl_timer.timeout.connect(self._on_ttl_timeout)
        self._ttl = 1000

        self._text = ""

        self._font = self.font()
        self._font.setPointSize(18)
        self.setFont(self._font)

        self._group_anim = QtCore.QParallelAnimationGroup()

        self._text_animation = QtCore.QPropertyAnimation(self, 'textColor')
        self._text_animation.setDuration(1000)
        fgcolor = self.palette().color(QtGui.QPalette.Text)
        self._text_animation.setStartValue(fgcolor)
        fgcolor.setAlphaF(0)
        self._text_animation.setEndValue(fgcolor)
        self._group_anim.addAnimation(self._text_animation)

        self._bg_animation = QtCore.QPropertyAnimation(self, 'backgroundColor')
        self._bg_animation.setDuration(1000)
        bgcolor = self.palette().color(QtGui.QPalette.Window)
        self._bg_animation.setStartValue(bgcolor)
        bgcolor.setAlphaF(0)
        self._bg_animation.setEndValue(bgcolor)
        self._group_anim.addAnimation(self._bg_animation)
        self._group_anim.stateChanged.connect(self._on_anim_changed)
        self._update_position()

    def setOwner(self, owner):
        '''
        Sets the owner of the notification widget.

        :param owner: Widget to follow. Can be thought of as a parent widget, but without the Qt implications.
        '''
        self._owner = owner

    def _get_screen(self):
        owner = self._owner
        if owner is None:
            owner = self
        desktop = QtGui.QApplication.desktop()
        return desktop.screen(desktop.screenNumber(owner))

    def _update_position(self):
        screen_widget = self._get_screen()
        offset = screen_widget.pos()
        if self._pos == self.POSITION_TOP_LEFT:
            pass
        elif self._pos == self.POSITION_TOP_CENTER:
            offset.setX(offset.x() + screen_widget.width() * 0.5 - self.width() * 0.5)
        elif self._pos == self.POSITION_TOP_RIGHT:
            offset.setX(offset.x() + screen_widget.width() - self.width())
        elif self._pos == self.POSITION_CENTER_LEFT:
            offset.setY(offset.y() + screen_widget.height() * 0.5 - self.height() * 0.5)
        elif self._pos == self.POSITION_CENTER_CENTER:
            offset.setY(offset.y() + screen_widget.height() * 0.5 - self.height() * 0.5)
            offset.setX(offset.x() + screen_widget.width() * 0.5 - self.width() * 0.5)
        elif self._pos == self.POSITION_CENTER_RIGHT:
            offset.setY(offset.y() + screen_widget.height() * 0.5 - self.height() * 0.5)
            offset.setX(offset.x() + screen_widget.width() - self.width())
        elif self._pos == self.POSITION_BOTTOM_LEFT:
            offset.setY(offset.y() + screen_widget.height() - self.height())
        elif self._pos == self.POSITION_BOTTOM_CENTER:
            offset.setY(offset.y() + screen_widget.height() - self.height())
            offset.setX(offset.x() + screen_widget.width() * 0.5 - self.width() * 0.5)
        elif self._pos == self.POSITION_BOTTOM_RIGHT:
            offset.setY(offset.y() + screen_widget.height() - self.height())
            offset.setX(offset.x() + screen_widget.width() - self.width())
        self.move(offset)

    def setPosition(self, pos):
        '''
        Sets the position of the notification widget relative to the screen of the owner widget.

        :param pos: One of the POSITION_* constants
        '''
        self._pos = pos

    def mousePressEvent(self, event):
        self.close()

    def resizeEvent(self, event):
        self._update_position()

    def setText(self, text):
        '''
        Sets the text of the notification widget.
        Setting the text will reset the internal state and show the notification immediately

        :param text: Text to show. Will be trimmed according to fix screen.
        '''
        self._text = text
        if text:
            fm = QtGui.QFontMetrics(self._font)
            text_list = text.split('\n')
            width = 0
            screen_width = self._get_screen().width()
            trimmed = []
            for t in text_list:
                w = fm.width(t)
                if w > screen_width:
                    while w > screen_width:
                        t = t[:len(t) - 1]
                        w = fm.width(t)
                    t = '{0}{1}'.format(t[:len(t) - 3], '...')
                    w = fm.width(t)
                if w > width:
                    width = w
                trimmed.append(t)
            self._text = '\n'.join(trimmed)
            height = fm.height() * (len(text_list))
            self.resize(width, height)
            self._update_position()
            self._restart()
        else:
            self._ttl_timer.stop()
            self._group_anim.stop()
            self.hide()

    def _restart(self):
        self._group_anim.setCurrentTime(0)
        # force a reset by briefly playing the animation
        self._group_anim.start()
        self._group_anim.stop()
        self._group_anim.setCurrentTime(0)
        self._ttl_timer.start(self._ttl)
        self.show()
        self.update()

    def _on_ttl_timeout(self):
        self._group_anim.stop()
        self._group_anim.start()

    def _on_anim_changed(self, new_state, old_state):
        if new_state == QtCore.QAbstractAnimation.Stopped:
            self.hide()
        elif new_state == QtCore.QAbstractAnimation.Running:
            self.show()

    def setFont(self, font):
        '''
        Sets the font of the notification widget

        :param font: The new font of the notification widget.
        '''
        self._font = font
        fm = QtGui.QFontMetrics(self._font)
        self.resize(self.width(), fm.height())
        self._update_position()

    def _set_text_color(self, color):
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Text, color)
        self.setPalette(palette)

    def _get_text_color(self):
        return self.palette().color(QtGui.QPalette.Text)

    def _set_bg_color(self, color):
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, color)
        self.setPalette(palette)

    def _get_bg_color(self):
        return self.palette().color(QtGui.QPalette.Window)

    def setTtl(self, ttl, fadeout=0):
        '''
        Sets the time until the notification should be hidden.

        :param ttl: The time in milliseconds until the notification should be hidden.
        :param fadeout: Fadeout duration in milliseconds, cannot be longer than ttl.
        '''

        if fadeout > ttl:
            fadeout = ttl
        self._ttl = ttl - fadeout
        self._fade_animation.setDuration(fadeout)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.save()
        rect = self.rect()
        painter.setClipRect(rect)
        bgcolor = self.palette().color(QtGui.QPalette.Window)
        fgcolor = self.palette().color(QtGui.QPalette.Text)
        painter.fillRect(rect, bgcolor)
        pen = painter.pen()
        pen.setColor(fgcolor)
        painter.setPen(pen)
        if self._text:
            font = painter.font()
            font.setPointSizeF(self._font.pointSizeF())
            painter.setFont(font)
            painter.drawText(rect, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, self._text)
        painter.restore()

    textColor = QtCore.Property(QtGui.QColor, _get_text_color, _set_text_color)
    '''text color property'''

    backgroundColor = QtCore.Property(QtGui.QColor, _get_bg_color, _set_bg_color)
    '''background color property'''
