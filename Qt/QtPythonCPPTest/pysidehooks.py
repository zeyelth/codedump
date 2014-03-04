def mainwindow():
    import pysidehooks_impl
    from PySide import QtGui, shiboken
    return shiboken.wrapInstance(pysidehooks_impl.mainwindow(), QtGui.QMainWindow)
