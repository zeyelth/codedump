QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

QMAKE_CXXFLAGS += -std=c++11

CONFIG += plugin

TARGET = qt_enum_prop_repro

TEMPLATE = lib

SOURCES += main.cpp\
        mainwindow.cpp \
    myplugin.cpp

HEADERS  += mainwindow.h \
    myplugin.h \
    mywidget.h

FORMS    += mainwindow.ui
