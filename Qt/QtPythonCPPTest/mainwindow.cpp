/*
Copyright (c) 2013-2014 Victor Wåhlström

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
*/


#include <QtCore>
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <boost/python.hpp>

QMainWindow* g_mainWindow = 0;

size_t mainWindow()
{
    return (size_t)g_mainWindow;
}

BOOST_PYTHON_MODULE(pysidehooks_impl)
{
    boost::python::def("mainwindow", mainWindow);
}

void init_python()
{
    Py_Initialize();
    initpysidehooks_impl();
    QDir module_dir = QDir(qApp->applicationDirPath());
    module_dir.cd("modules");
    QString setup_script = "import os, sys; sys.path.insert(0, '";
    setup_script.append(module_dir.absolutePath());
    setup_script.append("')");
    QByteArray data = setup_script.toLocal8Bit();
    if(PyRun_SimpleString(data.constData()) != 0)
    {
        PyErr_Print();
    }
}

void destroy_python()
{
    Py_Finalize();
}

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    g_mainWindow = this;
    QObject::connect(ui->actionReload, SIGNAL(triggered()), this, SLOT(reload()));

    init_python();
}

void MainWindow::reload()
{
    QByteArray data = ui->textEdit->toPlainText().toLocal8Bit();
    if(PyRun_SimpleString(data.constData()) != 0)
    {
        PyErr_Print();
    }
}

MainWindow::~MainWindow()
{
    destroy_python();
    delete ui;
    g_mainWindow = 0;
}
