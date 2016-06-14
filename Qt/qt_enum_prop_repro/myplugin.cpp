#include "myplugin.h"
#include "mywidget.h"


MyPlugin::MyPlugin(QObject *parent)
    : QObject(parent),
      initialized(false)
{
}

void MyPlugin::initialize(QDesignerFormEditorInterface*)
{
    if (initialized)
        return;

    initialized = true;
}

bool MyPlugin::isInitialized() const
{
    return initialized;
}

QWidget* MyPlugin::createWidget(QWidget* parent)
{
    return new MyWidget(parent);
}

QString MyPlugin::name() const
{
    return "MyWidget";
}

QString MyPlugin::group() const
{
    return "Input Widgets";
}

QIcon MyPlugin::icon() const
{
    return QIcon();
}

QString MyPlugin::toolTip() const
{
    return "Repro case for strongly typed enum property issue";
}

QString MyPlugin::whatsThis() const
{
    return "Repro case for strongly typed enum property issue";
}

bool MyPlugin::isContainer() const
{
    return false;
}

QString MyPlugin::domXml() const
{
    return "<ui language=\"c++\">\n"
           " <widget class=\"MyWidget\" name=\"myWidget\">\n"
           "  <property name=\"geometry\">\n"
           "   <rect>\n"
           "    <x>0</x>\n"
           "    <y>0</y>\n"
           "    <width>100</width>\n"
           "    <height>25</height>\n"
           "   </rect>\n"
           "  </property>\n"
           "  <property name=\"toolTip\" >\n"
           "   <string></string>\n"
           "  </property>\n"
           "  <property name=\"whatsThis\" >\n"
           "   <string></string>\n"
           "  </property>\n"
           " </widget>\n"
           "</ui>\n";
}

QString MyPlugin::includeFile() const
{
    return "mywidget.h";
}

