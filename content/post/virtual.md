---
title:  "Virtual Functions"
date:   2023-06-04T21:28:51+08:00
summary: "This short article explains what are virtual functions and why we need them."
tags: ['virtual functions','class']
draft:  false
---

我们先来看以下例子。

```cpp
#include <iostream>
#include <string>
using namespace std;

class Person
{
  public:
    string name;
    Person(string n): name(n){}
    void print()
    {
        cout << "Name: " << name << endl;
    }
};
class Student: public Person
{
  public:
    string id;
    Student(string n, string i): Person(n), id(i){}
    void print() 
    {
        cout << "Name: " << name;
        cout << ". ID: " << id << endl;
    }
};
void printObjectInfo(Person & p)
{
    p.print();
}
```

我们在父类和子类中都定义了`print`函数，那么此时

```cpp
Person * p = new Student("xue", "2020");
p->print(); //if print() is not a virtual function, different output
delete p; //if its destructor is not virtual
```

`p->print()`肯定会调用父类的`print()`函数，这是符合逻辑的。类似的，

```cpp
Student stu("yu", "2019");
printObjectInfo(stu);  
```

也会调用父类的`print()`函数。

但是，我们或许会希望，`printObjectInfo()`只是作为一个代号，调用这个函数时的输入可以是所有`Person()`类的派生类（子类），其中使用的函数自动识别为子类的对应函数。这种想法听起来好像天方夜谭，但实际上是可以做到的。我们只需要在父类的`print()`函数之前加一个`virtual`关键词，便可达到这样的效果，即

```cpp
class Person
{
  public:
    string name;
    Person(string n): name(n){}
    virtual void print()
    {
        cout << "Name: " << name << endl;
    }
};
```

此时，不论是`p->print();`还是`printObjectInfo(stu); `都会调用子类的`print()`函数。

这是怎么做到的呢？它的原理是，一旦出现了`virtual`关键词，那么每一个`Person`类或者其派生类的对象被创建的时候，都会自动生成一个隐藏的指针，指向函数表。这个函数表记录着此时对象所拥有的函数；`virtual`函数在接收对象时会根据这个隐藏指针所指向的函数调用相应的函数。因此，
- 尽管`p`是一个`Person`类的对象，但他是通过`Student`的构造函数创建的，此时隐藏指针指向的就是`Student::print()`; 
- 类似的，虽然`printObjectInfo()`的输入参数是一个`Person`对象的引用，但是它是通过`Student`对象初始化的，因此他的隐藏指针指向的也是`Student::print()`.

事实上，所有析构函数（destructor）都是`virtual`函数，这样在释放内存的时候才不会出错。

本节的视频讲解参见[Bilibili - 于仕琪老师的C/C++从基础语法到优化策略课程](https://www.bilibili.com/video/BV1Vf4y1P7pq/?spm_id_from=333.999.0.0)第12.4节。