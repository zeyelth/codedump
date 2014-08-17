import sys
from PySide import QtGui
from colorpicker import ColorPicker
import logging

logger = logging.getLogger('colorpicker_example')
logger.setLevel(logging.DEBUG)


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        central_widget = QtGui.QWidget()

        self._stylesheet = "color: {}; background-color: {}"

        layout = QtGui.QFormLayout()
        self._lbl1 = QtGui.QLabel()
        self._lbl1.setText('Foreground')
        self._fg_color = ColorPicker()
        self._fg_color.colorChanged.connect(self._update_foreground)

        layout.addRow(self._lbl1, self._fg_color)

        self._lbl2 = QtGui.QLabel()
        self._lbl2.setText('Background')
        self._bg_color = ColorPicker()
        self._bg_color.colorChanged.connect(self._update_background)

        self._fg_color.setColor(QtGui.QColor(0, 0, 0))
        self._bg_color.setColor(QtGui.QColor(255, 255, 255))

        layout.addRow(self._lbl2, self._bg_color)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _color_to_hex(self, color):
        r = color.red()
        g = color.green()
        b = color.blue()

        return "#{1:0{0}x}{2:0{0}x}{3:0{0}x}".format(2, r, g, b)

    def _update_foreground(self, color):
        logger.log(logging.DEBUG,
                   "Updating fg_color: {}".format(self._color_to_hex(color)))
        self._update_stylesheet()

    def _update_background(self, color):
        logger.log(logging.DEBUG,
                   "Updating bg_color: {}".format(self._color_to_hex(color)))
        self._update_stylesheet()

    def _update_stylesheet(self):
        c1 = self._color_to_hex(self._fg_color.color())
        c2 = self._color_to_hex(self._bg_color.color())
        self.setStyleSheet(self._stylesheet.format(c1, c2))

if __name__ == '__main__':
    logging.basicConfig()
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()
