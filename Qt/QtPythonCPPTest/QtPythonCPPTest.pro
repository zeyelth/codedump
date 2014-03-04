#-------------------------------------------------
#
# Project created by QtCreator 2013-11-17T10:14:42
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = QtTest
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui

LIBS += -lpython2.7
LIBS += -lboost_python

#win32:CONFIG(release, debug|release): LIBS += -L$$OUT_PWD/../pysidehooks/release/ -lpysidehooks
#else:win32:CONFIG(debug, debug|release): LIBS += -L$$OUT_PWD/../pysidehooks/debug/ -lpysidehooks
#else:unix: LIBS += -L$$OUT_PWD/../pysidehooks/ -lpysidehooks

INCLUDEPATH += /usr/include/python2.7
#INCLUDEPATH += $$PWD/../pysidehooks
#DEPENDPATH += $$PWD/../pysidehooks

OTHER_FILES += \
    pysidehooks.py

#unix {
#    QMAKE_POST_LINK += $$quote(cp $${PWD}/pysidehooks.py $${DESTDIR}$$escape_expand(\\n\\t))
#}
