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
import math


def _draw_checkerboard(painter, rect, size):
    color1 = QtGui.QColor(153, 153, 152)
    color2 = QtGui.QColor(102, 102, 102)

    painter.save()
    painter.fillRect(rect, color1)
    square = QtCore.QRect(0, 0, size, size)
    step_x = size * 2
    step_y = size
    odd = True
    while square.top() < rect.bottom():
        while square.left() < rect.right():
            painter.fillRect(square, color2)
            square.moveLeft(square.left() + step_x)
        square.moveLeft(0)
        if odd:
            square.moveLeft(square.left() + step_x / 2.0)
        square.moveTop(square.top() + step_y)
        odd = not odd
    painter.restore()


class ColorWidget(QtGui.QWidget):
    """
    Base class for widgets manipulating colors.
    """

    colorChanged = QtCore.Signal(QtGui.QColor)
    """
    Emitted when the color has changed. Contains a matching QColor.
    """

    def __init__(self, parent=None):
        super(ColorWidget, self).__init__(parent)

        self._color = QtGui.QColor()

    def color(self):
        """
        The QColor represented by this widget.
        :return: A color
        :rtype: QColor
        """
        return QtGui.QColor(self._color)

    def updateColor(self, color):
        """
        Updates the color represented by this widget.
        Does not emit a signal.
        :param color: The new color.
        :type color: QColor
        """
        self._color = QtGui.QColor(color)
        self.repaint()

    def setColor(self, color):
        """
        Updates the color represented by this widget.
        Emits a colorChanged signal.
        :param color: The new color.
        :type color: QColor
        """
        self.updateColor(color)
        self.colorChanged.emit(self.color())


class ColorPicker(ColorWidget):
    """
    A compact color picker widget with a hue, and saturation wheel.
    Additional sliders for value, red, green, blue and alpha channels.
    """

    def __init__(self, parent=None):
        """
        Constructs a ColorPicker instance.
        :param parent: parent widget (optional)
        """
        super(ColorWidget, self).__init__(parent)

        layout = QtGui.QVBoxLayout()
        self._hex = ColorHexEdit()

        self._display = ColorDisplay()
        self._display.setMinimumSize(15, 15)
        size_policy = QtGui.QSizePolicy()
        size_policy.setHorizontalPolicy(QtGui.QSizePolicy.Minimum)
        self._display.setSizePolicy(size_policy)

        top_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(self._display)
        top_layout.addWidget(self._hex)
        top_layout.addStretch(100)

        self._wheel = HueSaturationWheel()
        size_policy = QtGui.QSizePolicy()
        size_policy.setVerticalPolicy(QtGui.QSizePolicy.Expanding)
        size_policy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
        self._wheel.setSizePolicy(size_policy)

        size = 10

        self._value_slider = ComponentSlider(ComponentSlider.hsvValue)
        self._value_slider.setMinimumWidth(size)
        self._value_slider.setDirection(ComponentSlider.Vertical)
        self._value_slider.setGradient(QtCore.Qt.black, QtCore.Qt.white)

        self._red_slider = ComponentSlider(ComponentSlider.rgbaRed)
        self._red_slider.setMinimumHeight(size)
        self._red_slider.setMaximumHeight(size)
        self._red_slider.setContentsMargins(4, 0, 0, 0)
        self._red_slider.setDirection(ComponentSlider.Horizontal)
        self._red_slider.setGradient(QtCore.Qt.black, QtCore.Qt.red)

        self._green_slider = ComponentSlider(ComponentSlider.rgbaGreen)
        self._green_slider.setMinimumHeight(size)
        self._green_slider.setMaximumHeight(size)
        self._green_slider.setDirection(ComponentSlider.Horizontal)
        self._green_slider.setGradient(QtCore.Qt.black, QtCore.Qt.green)

        self._blue_slider = ComponentSlider(ComponentSlider.rgbaBlue)
        self._blue_slider.setMinimumHeight(size)
        self._blue_slider.setMaximumHeight(size)
        self._blue_slider.setDirection(ComponentSlider.Horizontal)
        self._blue_slider.setGradient(QtCore.Qt.black, QtCore.Qt.blue)

        self._alpha_slider = ComponentSlider(ComponentSlider.rgbaAlpha)
        self._alpha_slider.setMinimumHeight(size)
        self._alpha_slider.setMaximumHeight(size)
        self._alpha_slider.setDirection(ComponentSlider.Horizontal)
        self._alpha_slider.setGradient(QtGui.QColor(255, 255, 255, 0), QtGui.QColor(255, 255, 255, 255))

        mid_layout = QtGui.QHBoxLayout()
        mid_layout.addWidget(self._wheel)
        mid_layout.addWidget(self._value_slider)

        font = QtGui.QFont("Monospace")
        font.setStyleHint(QtGui.QFont.TypeWriter)

        label = QtGui.QLabel("R")
        label.setFont(font)
        label.setMaximumHeight(size)
        label.setMinimumWidth(10)
        label.setMaximumWidth(10)
        r_layout = QtGui.QHBoxLayout()
        r_layout.addWidget(label)
        r_layout.addWidget(self._red_slider)

        label = QtGui.QLabel("G")
        label.setFont(font)
        label.setMaximumHeight(size)
        label.setMinimumWidth(10)
        label.setMaximumWidth(10)
        g_layout = QtGui.QHBoxLayout()
        g_layout.addWidget(label)
        g_layout.addWidget(self._green_slider)

        label = QtGui.QLabel("B")
        label.setFont(font)
        label.setMaximumHeight(size)
        label.setMinimumWidth(10)
        label.setMaximumWidth(10)
        b_layout = QtGui.QHBoxLayout()
        b_layout.addWidget(label)
        b_layout.addWidget(self._blue_slider)

        label = QtGui.QLabel("A")
        label.setFont(font)
        label.setMaximumHeight(size)
        label.setMinimumWidth(10)
        label.setMaximumWidth(10)
        a_layout = QtGui.QHBoxLayout()
        a_layout.addWidget(label)
        a_layout.addWidget(self._alpha_slider)

        bottom_layout = QtGui.QVBoxLayout()
        bottom_layout.setSpacing(2)
        bottom_layout.addLayout(r_layout)
        bottom_layout.addLayout(g_layout)
        bottom_layout.addLayout(b_layout)
        bottom_layout.addLayout(a_layout)

        layout.addLayout(top_layout)
        layout.addLayout(mid_layout)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        self._connection_list = [self._wheel,
                          self._hex,
                          self._display,
                          self._value_slider,
                          self._red_slider,
                          self._green_slider,
                          self._blue_slider,
                          self._alpha_slider]

        for x in self._connection_list:
            x.colorChanged.connect(self._color_broadcaster)
            x.colorChanged.connect(self.colorChanged)

        self._wheel.setColor(QtGui.QColor(255, 255, 255, 255))

    def _color_broadcaster(self, color):
        for x in self._connection_list:
            if x is not self.sender():
                x.updateColor(color)


class ColorHexEdit(ColorWidget):
    """
    A text editing widget, configured to manipulate color values on the form of #AARRGGBB,
    where AA, RR, GG, and BB represents the alpha, red, green and blue channels.
    """

    def __init__(self, parent=None):
        """
        Constructs a ColorHexEdit instance.
        :param parent: parent widget (optional)
        """
        super(ColorHexEdit, self).__init__(parent)

        layout = QtGui.QHBoxLayout()
        layout.setSpacing(0)

        hash_label = QtGui.QLabel()
        hash_label.setText("#")
        layout.addWidget(hash_label)

        self._line_edit = QtGui.QLineEdit()
        self._line_edit.setInputMask("HHHHHHHH")
        self._line_edit.setPlaceholderText("AARRGGBB")
        self._line_edit.setToolTip(self.tr("A hexadecimal value on the form AARRGGBB:\n\nAA = alpha\nRR = red\nGG = green\nBB = blue"))
        font = QtGui.QFont("Monospace")
        font.setStyleHint(QtGui.QFont.TypeWriter)
        self._line_edit.setFont(font)

        self.updateColor(self.color())

        self._line_edit.textEdited.connect(self._on_text_edited)

        layout.addWidget(self._line_edit)
        self.setLayout(layout)

    def _color_to_string(self, color):
        a = color.alpha()
        r = color.red()
        g = color.green()
        b = color.blue()

        return "{1:0{0}x}{2:0{0}x}{3:0{0}x}{4:0{0}x}".format(2, a, r, g, b)

    def updateColor(self, color):
        """
        Overridden from base class.
        Updates the text string to match the provided color.
        :param color: The new color.
        :type color: QColor
        """
        self._line_edit.setText(self._color_to_string(color))
        super(ColorHexEdit, self).updateColor(color)

    def _on_text_edited(self, text):
        if len(text) != 8:
            return

        if text == self._color_to_string(self._color):
            return

        a = int(text[0:2], 16)
        r = int(text[2:4], 16)
        g = int(text[4:6], 16)
        b = int(text[6:8], 16)

        color = QtGui.QColor(r, g, b, a)

        self._color = color
        self.colorChanged.emit(self._color)


class ColorDisplay(ColorWidget):
    """
    A simple widget for displaying a color, including alpha values.
    """

    clicked = QtCore.Signal()
    """
    Emitted when the widget is clicked on.
    """

    def __init__(self, parent=None):
        """
        Constructs a ColorDisplay instance.
        :param parent: parent widget (optional)
        """
        super(ColorDisplay, self).__init__(parent)

    def mouseReleasedEvent(self, event):
        self.clicked.emit()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.save()
        rect = self.rect()
        painter.setClipRect(rect)

        _draw_checkerboard(painter, rect, 5)

        painter.fillRect(rect, self._color)

        painter.restore()


class ComponentSlider(ColorWidget):
    """
    A custom slider for manipulating a color component.
    Although it only manipulates a single component, it holds a QColor for convenience.
    """

    Horizontal = 0
    Vertical = 1
    """
    Direction of the slider.
    """

    hsvHue = 0
    hsvValue = 1
    hsvSaturation = 2
    rgbaRed = 3
    rgbaGreen = 4
    rgbaBlue = 5
    rgbaAlpha = 6
    """
    Supported QColor components.
    """

    def __init__(self, component, parent=None):
        """
        Constructs a ComponentSlider instance.
        :param component: The component managed by this slider.
        :type component: Any of class variables hsvHue, hsvValue, hsvSaturation, rgbaRed, rgbaGreen, rgbaBlue, rgbaAlpha
        :param parent: parent widget (optional)
        """
        super(ComponentSlider, self).__init__(parent)

        self._direction = self.Horizontal

        self._gradient_color1 = QtCore.Qt.white
        self._gradient_color2 = QtCore.Qt.black
        self._component = component

    def setActiveComponent(self, component):
        """
        Sets the color component managed by this slider.
        :param component: The new component.
        :type component: Any of class variables hsvHue, hsvValue, hsvSaturation, rgbaRed, rgbaGreen, rgbaBlue, rgbaAlpha
        :type color: QColor
        """
        self._component = component

    def setDirection(self, direction):
        """
        Sets the direction of this slider.
        :param direction: The direction.
        :type direction: Either of the class variables Horizontal, and Vertical.
        """
        self._direction = direction

    def setGradient(self, color1, color2):
        """
        Sets the color gradient of this slider's visual representation.
        :param color1: The first color of the gradient.
        :param color2: The second color of the gradient.
        """
        self._gradient_color1 = color1
        self._gradient_color2 = color2

    def _clamp(self, val, minimum, maximum):
        if val < minimum:
            val = minimum
        elif val > maximum:
            val = maximum
        return val

    def _get_component_value(self):
        if self._component == self.rgbaRed:
            return self._color.redF()
        if self._component == self.rgbaGreen:
            return self._color.greenF()
        if self._component == self.rgbaBlue:
            return self._color.blueF()
        if self._component == self.rgbaAlpha:
            return self._color.alphaF()
        if self._component == self.hsvHue:
            return self._color.hsvHueF()
        if self._component == self.hsvSaturation:
            return self._color.hsvSaturationF()
        if self._component == self.hsvValue:
            return self._color.valueF()

    def _update_color(self, pos):
        if self._component not in [self.rgbaRed,
                                   self.rgbaGreen,
                                   self.rgbaBlue,
                                   self.rgbaAlpha,
                                   self.hsvHue,
                                   self.hsvSaturation,
                                   self.hsvValue]:
            return

        rect = self.rect()

        if self._direction == self.Vertical:
            component_value = 1 - float(self._clamp(pos.y(), rect.top(), rect.bottom())) / float(rect.bottom() - rect.top())
        else:
            component_value = float(self._clamp(pos.x(), rect.left(), rect.right())) / float(rect.right() - rect.left())

        if self._component in [self.rgbaRed, self.rgbaGreen, self.rgbaBlue, self.rgbaAlpha]:
            c = self._component
            r = component_value if c == self.rgbaRed else self._color.redF()
            g = component_value if c == self.rgbaGreen else self._color.greenF()
            b = component_value if c == self.rgbaBlue else self._color.blueF()
            a = component_value if c == self.rgbaAlpha else self._color.alphaF()
            self._color.setRgbF(r, g, b)
            self._color.setAlphaF(a)
        else:
            c = self._component
            a = self._color.alphaF()
            h = component_value if c == self.hsvHue else self._color.hsvHueF()
            s = component_value if c == self.hsvSaturation else self._color.hsvSaturationF()
            v = component_value if c == self.hsvValue else self._color.valueF()
            self._color.setHsvF(h, s, v)
            self._color.setAlphaF(a)

        self.repaint()

    def mousePressEvent(self, event):
        self._update_color(event.pos())
        self.colorChanged.emit(self._color)

    def mouseMoveEvent(self, event):
        self._update_color(event.pos())
        self.colorChanged.emit(self._color)

    def mouseReleaseEvent(self, event):
        self._update_color(event.pos())

    def paintEvent(self, event):
        rect = self.rect()
        painter = QtGui.QPainter(self)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setClipRect(rect)

        size = min(rect.width(), rect.height()) * 0.5
        _draw_checkerboard(painter, rect, size)

        if self._direction == self.Vertical:
            gradient = QtGui.QLinearGradient(rect.bottomLeft(), rect.topLeft())
        else:
            gradient = QtGui.QLinearGradient(rect.topLeft(), rect.topRight())
        gradient.setColorAt(0, self._gradient_color1)
        gradient.setColorAt(1, self._gradient_color2)
        painter.fillRect(rect, gradient)

        if self._direction == self.Vertical:
            pos = rect.height() - self._get_component_value() * (rect.bottom() - rect.top())
            line2 = QtCore.QLineF(rect.left(), pos, rect.right(), pos)
            line1 = line2.translated(0, -1)
            line3 = line2.translated(0, 1)
        else:
            pos = self._get_component_value() * (rect.right() - rect.left())
            line2 = QtCore.QLineF(pos, rect.top(), pos, rect.bottom())
            line1 = line2.translated(-1, 0)
            line3 = line2.translated(1, 0)

        pen = QtGui.QPen()
        pen.setWidth(1)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, False)

        pen.setColor(QtGui.QColor(0, 0, 0))
        painter.setPen(pen)
        painter.drawLine(line1)
        pen.setColor(QtGui.QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawLine(line2)
        pen.setColor(QtGui.QColor(0, 0, 0))
        painter.setPen(pen)
        painter.drawLine(line3)

        painter.restore()


class HueSaturationWheel(ColorWidget):
    """
    A color wheel for manipulating the hue and saturation of a given QColor.
    """

    def __init__(self, parent=None):
        """
        Constructs a HueSaturationWheel instance.
        :param parent: parent widget (optional)
        """
        super(HueSaturationWheel, self).__init__(parent)

        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._color = QtGui.QColor(255, 255, 255)
        self._wheel_img = None
        self._marker_pos = QtCore.QPointF(0, 0)

    def updateColor(self, color):
        """
        Updates the color represented by this widget.
        Does not emit a signal.
        :param color: The new color.
        :type color: QColor
        """

        if color.rgb() == self._color.rgb():
            return

        old_value = self._color.value()

        square = self._square()

        radius = square.width() * 0.5

        hue = color.hsvHueF()
        sat = color.hsvSaturationF()

        self._color.setRgba(color.rgba())

        distance = sat * radius

        center = square.center()
        line = QtCore.QLineF(center.x(), center.y(), center.x(), center.y() + distance)
        line.setAngle(360.0 - hue * 360.0)
        line.setAngle(line.angle() - 90)

        self._update_color(line.p2())
        self._update_marker_pos()
        if old_value != color.value():
            self._rebuild_color_wheel()

        super(HueSaturationWheel, self).updateColor(color)

    def _length2(self, p1, p2):
        return pow((p2.x() - p1.x()), 2) + pow((p2.y() - p1.y()), 2)

    def _length(self, p1, p2):
        return math.sqrt(self._length2(p1, p2))

    def _update_color(self, pos):
        square = self._square()

        radius = square.width() * 0.5
        line = QtCore.QLineF(square.center(), pos)
        distance = self._length(line.p1(), line.p2())
        if distance > radius:
            distance = radius
        line.setAngle(line.angle() + 90.0)
        h = (360.0 - line.angle()) / 360.0
        s = distance / radius
        v = self._color.valueF()
        a = self._color.alphaF()
        self._color.setHsvF(h, s, v)
        self._color.setAlphaF(a)

    def _square(self):
        rect = self.rect()
        w = rect.width()
        h = rect.height()
        if w > h:
            offset = (w - h) * 0.5
            rect.setWidth(h)
            rect.moveLeft(rect.left() + offset)
        else:
            offset = (h - w) * 0.5
            rect.setHeight(w)
            rect.moveTop(rect.top() + offset)
        return rect

    def _update_marker_pos(self):
        square = self._square()

        radius = square.width() * 0.5

        hue = self._color.hsvHueF()
        sat = self._color.hsvSaturationF()

        distance = sat * radius

        center = square.center()
        line = QtCore.QLineF(center.x(), center.y(), center.x(), center.y() + distance)
        line.setAngle(360.0 - hue * 360.0)
        line.setAngle(line.angle() - 90)

        self._marker_pos = line.p2()

    def _rebuild_color_wheel(self):
        self._wheel_img = QtGui.QImage(self._square().size(), QtGui.QImage.Format_ARGB32_Premultiplied)
        self._wheel_img.fill(0)
        rect = self._wheel_img.rect()
        painter = QtGui.QPainter(self._wheel_img)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen()
        pen.setColor(QtCore.Qt.transparent)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.transparent)
        painter.drawRect(rect)

        radius = rect.width() * 0.5
        path = QtGui.QPainterPath()
        path.addEllipse(rect)

        painter.setClipPath(path)

        # hue, value
        hue = QtGui.QConicalGradient(rect.center(), -90)
        color = QtGui.QColor()
        step = 0
        value = self._color.valueF()
        while step < 1.0:
            color.setHsvF(1 - step, 1, value)
            hue.setColorAt(step, color)
            step += 0.1
        painter.fillPath(path, hue)

        # saturation. A bit hackish and may not be pixel perfect, but it's only used as a visual representation...
        saturation = QtGui.QRadialGradient(rect.center(), radius)
        color.setRgbF(value, value, value)
        color.setAlphaF(1)
        saturation.setColorAt(0, color)
        color.setRgbF(value, value, value)
        color.setAlphaF(0)
        saturation.setColorAt(1, color)
        painter.fillPath(path, saturation)
        painter.restore()

        self.repaint()

    def resizeEvent(self, event):
        self._rebuild_color_wheel()
        self._update_marker_pos()
        return super(HueSaturationWheel, self).resizeEvent(event)

    def mousePressEvent(self, event):
        self._update_color(event.pos())
        self._update_marker_pos()
        self.repaint()
        self.colorChanged.emit(self.color())

    def mouseMoveEvent(self, event):
        self._update_color(event.pos())
        self._update_marker_pos()
        self.repaint()
        self.colorChanged.emit(self.color())

    def mouseReleaseEvent(self, event):
        self._update_color(event.pos())
        self._update_marker_pos()
        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setClipRect(self.rect())

        painter.drawImage(self._square(), self._wheel_img)

        pen = QtGui.QPen()
        v = 0 if self._color.valueF() > 0.5 else 255
        pen.setColor(QtGui.QColor(v, v, v))
        painter.setPen(pen)
        marker = QtCore.QRectF(self._marker_pos.x() - 2, self._marker_pos.y() - 2, 5, 5)
        painter.drawArc(marker, 0, 5760)  # angles are specified in 1/16 of a degree; draws a full circle

        painter.restore()
