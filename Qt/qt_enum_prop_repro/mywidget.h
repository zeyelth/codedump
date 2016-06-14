#ifndef MYWIDGET_H
#define MYWIDGET_H

#include <QtWidgets/QWidget>

class MyWidget : public QWidget
{
    Q_OBJECT

    Q_PROPERTY(MyEnum myProp READ myProp WRITE setMyProp)

public:

    MyWidget(QWidget* parent = Q_NULLPTR)
        : QWidget(parent), myprop(MyEnum::A) {}

    enum class MyEnum
    {
        A = 0,
        B = 1,
    };

    Q_ENUM(MyEnum)

    MyEnum myProp() { return myprop; }
    void setMyProp(MyEnum value) { myprop = value; }

private:
    MyEnum myprop;

};

#endif // MYWIDGET_H

