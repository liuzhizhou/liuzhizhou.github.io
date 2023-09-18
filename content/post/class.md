---
title:  "`class` for CPP"
date:   2023-06-03T16:41:22+08:00
summary:  "A detailed illustration for `class` in CPP."
tags:     ['C and CPP', 'class']
draft:  false
---

## `class`: intro

为了让`struct`的功能更丰富，CPP中出现了`class`的概念。它不仅有成员变量，而且还有成员函数。成员函数可以在类内给出定义，也可以只在类的内部进行申明，在类外再进行定义（需要明确类名，表示成员函数）。通常，我们会在定义成员变量前加入`private:`（默认也是`private`, 写上只是为了更加清晰），表示成员变量是私有的，不可以在类外直接访问。如果访问了，则会出现编译错误。例子如下：

```cpp
#include <cstring>
#include <iostream>

class Student
{
  private:
    char name[4];
    int born;
    bool male; 
  public:
    void setName(const char * s)
    {
        strncpy(name, s, sizeof(name));
    }
    void setBorn(int b)
    {
        born = b;
    }
    // the declarations, the definitions are out of the class
    void setGender(bool isMale);
    void printInfo();
};
void Student::setGender(bool isMale)
{
    male = isMale;
}
void Student::printInfo()
{
    std::cout << "Name: " << name << std::endl;
    std::cout << "Born in " << born << std::endl;
    std::cout << "Gender: " << (male ? "Male" : "Female") << std::endl;
}
```

一般来说，特别简单的函数会放在类的内部，其他相对复杂的放在类的外部。类的定义放在头文件`.hpp`文件中，函数放在`.cpp`文件中。

## Constructors（构造函数） and Destructors（析构函数）

### constructor

构造函数是每个class都必须有的函数，它负责对象的构造，如果没有写，那么编译器会自动生成一个空的构造函数。构造函数的名字必须与class的名字相同，且没有返回值；它可以被重载——只要函数的参数不同，我们可以定义多个不同的构造函数，比如：

```cpp
Student() // 默认构造函数
    {
        name[0] = 0;
        born = 0;
        male = false;
        cout << "Constructor: Person()" << endl;
    }
Student(const char * initName): born(0), male(true) // 转换构造函数
{
    setName(initName);
    cout << "Constructor: Person(const char*)" << endl;
}
Student(const char * initName, int initBorn, bool isMale) // 普通构造函数
{
    setName(initName);
    born = initBorn;
    male = isMale;
    cout << "Constructor: Person(const char, int , bool)" << endl;
}
```

这里我们通过不同输入参数`()`,`(const char * initName)`和`const char * initName, int initBorn, bool isMale`，写了三个构造函数，其中第二个写法只是为了节省代码行数，其等价于

```cpp
Student(const char * initName): 
{
    born = 0;
    male = true;
    setName(initName);
    cout << "Constructor: Person(const char*)" << endl;
}
```

构造函数会在创建对象时被调用。创建的对象可以是在栈(steak)上，也可以在堆(heap)上；这点和基本数据类型是同样的。比如在栈上创建一个`Student`对象：我们给出三个方法

```cpp
Student yu; // 调用默认构造函数
Student li("li"); // 调用转换构造函数，显式调用
Student xue = Student("Xue", 1962, true);// 调用普通构造函数
```

其中第二种方法和第三种方法分别等价于

```cpp
Student li = Student("li"); // 调用转换构造函数，显式调用
Student li = "li"; // 调用转换构造函数，隐式调用

Student xue("Xue", 1962, true); // 调用普通构造函数
```

这三种创建对象的方法会调用三个不同的构造函数。显式调用和隐式调用的区别是，如果在转换构造函数之前添加`explicit`关键词，则隐式调用会抱编译错误。举例言之，在`std::shared_ptr<T>`这个官方模版类中，其定义了`explicit shared_ptr<T>(T* p);`这个构造函数，因此在使用时

```cpp
MyTime * p = *(MyTime(10));
std::shared_ptr<MyTime> m1 = p; // error: 隐式调用转换构造函数
std::shared_ptr<MyTime> m1(p); // 编译通过
```

在堆上创建对象的方法也是类似的`new Student()`会给构造的对象申请相应大小的内存，通过赋值到一个指针上就完成了堆上对象的创建：

```cpp
Student * zhou =  new Student("Zhou", 1991, false);
zhou->printInfo();
delete zhou;
```

注意这里的`zhou`是一个指针，而非一个`Student`对象。因此在使用类函数时，我们用的是`->`.

#### default constructor

在使用

```cpp
Student yu;
```

创建对象时，我们没有指明我们想要使用的构造函数，此时，会调用默认构造函数 (default constructors)——没有参数列表的那个构造函数。如果我们没有定义任何构造函数，那么编译器会自动生成一个空的，这一点我们在这一部分开头就说过。但是一旦我们定义了一个有参数的构造函数，编译器就不会再默认生成了，此时如果调用默认构造函数，那么会出现编译错误。

#### copy constructor and default copy constructor

一个拷贝构造函数当然是一个构造函数，他的参数列表是它自身类型的引用，如下：

```cpp
MyTime::MyTime(MyTime & t){...}
```

这个拷贝构造函数可以帮助我们通过一个已有的对象来创建一个新的对象。如果用户没有定义拷贝构造函数，那么编译器会自动生成一个拷贝构造函数，这个自动生成的拷贝构造函数会将所有非`static`的成员变量拷贝一遍。

### destructor

现在我们介绍析构函数。
比如对于下面这个例子（与之前不同的是，`name`不再是数组，而是一个`char*`类型指针，我们必须统一为他申请一个堆上的内存）。

```cpp
class Student
{
  private:
    char * name;
    int born;
    bool male; 
  public:
    Student()
    {
        name = new char[1024]{0};
        born = 0;
        male = false;
        cout << "Constructor: Person()" << endl;
    }
    Student(const char * initName, int initBorn, bool isMale)
    {
        name =  new char[1024];
        setName(initName);
        born = initBorn;
        male = isMale;
        cout << "Constructor: Person(const char, int , bool)" << endl;
    }
    ~Student()
    {
        cout << "To destroy object: " << name << endl;
        delete [] name;
    }

    void setName(const char * s)
    {
        strncpy(name, s, 1024);
    }
    void setBorn(int b)
    {
        born = b;
    }
    // the declarations, the definitions are out of the class
    void setGender(bool isMale);
    void printInfo();
};
```

析构函数会是在对象销毁之前做一些事情。那么对象什么时候会被销毁呢？答案是
- 如果他是栈上的对象，那么就是在它离开他的作用域的时候，也就是直到它所对应的花括号`}`之时
- 如果他是堆上的对象，那就是delete它的时候。如果忘记delete了，那么析构函数不会被调用。

如果我们定义类时没有写析构函数，那么编译器会自动生成一个空的析构函数。

```cpp
~Student(){}
```

有一点需要注意的是，如果我们动态申请了一个类的数组，那么在delete的时候主要要使用`delete []`, 否则只会调用第一个对象的析构函数。

此时

```cpp
Student * class1 = new Student[3]{
        {"Tom", 2000, true},
        {"Bob", 2001, true},
        {"Amy", 2002, false},
};

class1[1].printInfo();
delete class1;
//delete []class1;
```

`delete class1`只会调用`class1[0]`的析构函数，那么此时虽然`class1`会被系统回收，但是`class1[1]`, `class1[2]`在构造时申请的1024字节(Bytes)的内存都不会被回收，造成了内存泄漏。使用`delete []class1`才能调用他们三个的析构函数。

## `this`指针

在类的定义时，我们可以`this`是一个指向当前类对应的对象的指针，有了它之后类的定义可以更加方便。比如之前的`Student(const char * initName, int initBorn, bool isMale)`可以改写为

```cpp
Student(const char * name, int born, bool male)
{
    this->name =  new char[1024];
    setName(name);
    this->born = born;
    this->male = male;
    cout << "Constructor: Person(const char, int , bool)" << endl;
}
```

如果不使用`this`只需要保证输入参数的名称和类的变量名不同，那么类就可以自动识别添加`this->`, 因此可以省略。

## `static` members

静态成员是一种不会被绑定到成员上的变量，它和对象无关，是所有对象公用的。静态函数也是，不需要对象创建也可以使用，所以说静态函数不能操作非静态变量。

```cpp
#include <iostream>
#include <cstring>

using namespace std;

class Student
{
  private:
    static size_t student_total; // declaration only
    //inline static size_t student_total = 0; //C++17, definition outside isn't needed
    char * name;
    int born;
    bool male; 
  public:
    Student()
    {
        student_total++;
        name = new char[1024]{0};
        born = 0;
        male = false;
        cout << "Constructor: Person(): student_total = " << student_total << endl;
    }
    Student(const char * initName, int initBorn, bool isMale)
    {
        student_total++;
        name =  new char[1024];
        setName(initName);
        born = initBorn;
        male = isMale;
        cout << "Constructor: Person(const char, int , bool): student_total = " << student_total << endl;
    }
    ~Student()
    {
        student_total--;
        cout << "To destroy object: " << name ;
        cout << ". Then " << student_total << " students are left" << endl;
        delete [] name;
    }

    void setName(const char * s)
    {
        strncpy(name, s, 1024);
    }
    void setBorn(int b)
    {
        born = b;
    }
    static size_t getTotal() {return student_total;}
};

size_t Student::student_total = 0; // definition it here

int main()
{

    Student * class1 = new Student[3]{
        {"Tom", 2000, true},
        {"Bob", 2001, true},
        {"Amy", 2002, false},
    };

    Student yu("Yu", 2000, true);
    delete []class1;

    return 0;
}
```

如果没有定义

```cpp
size_t Student::student_total = 0; 
```

则会报链接错误。如果怕忘记的话，可以使用C++17标准的g++, 在申明静态变量之前加入`inline`关键词，就可以省去后面的定义，即

```cpp
inline static size_t student_total = 0;
```

## Operator Overloading

运算符可以看作一个类中特殊的成员函数。下面的例子重载了MyTime类的加法运算符`+`和`+=`。

```cpp
class MyTime
{
    int hours;
    int minutes;
  public:
    MyTime(): hours(0), minutes(0){}
    MyTime(int h, int m): hours(h), minutes(m){}

    MyTime operator+(const MyTime & t) const
    {
        MyTime sum;
        sum.minutes = this->minutes + t.minutes;
        sum.hours = this->hours + t.hours;

        sum.hours +=  sum.minutes / 60;
        sum.minutes %= 60;
        
        return sum;
    }
    MyTime & operator+=(const MyTime & t) 
    {
        this->minutes += t.minutes;
        this->hours += t.hours;

        this->hours +=  this->minutes / 60;
        this->minutes %= 60;
        
        return *this;
    }
    std::string getTime() const
    {
        return std::to_string(this->hours) + " hours and " 
                + std::to_string(this->minutes) + " minutes.";
    }
};
```

上面例子中频繁出现了`const`关键词，关于这个部分的知识，可以参看我的博客[Keyword `const` in C and CPP](https://liuzhizhou.github.io/blog/const/). 

上面代码中存在一个疑问：为什么operator`+=`需要返回值呢？我们知道`+=`会改变符号左端的值，那么返回值的意义是什么？原因是因为`+=`符号是一个表达式 (expression), 表达式需要有值。

在调用时以下代码（`t1`,`t2`都是MyTime类型的变量）

```cpp
t1 += t2;
t1.operator+=(t2);
```

是等价的。

运算符既然能够被类重载，当然可以继续重载，只需要输入的参数类型不同即可。

## `friend` Functions (友元函数)

友元函数可以帮我们实现类似`20+t1`的功能。它

- 必须在类的内部申明；
- 能够访问类的变量，包括私有变量
- 它**不是**成员函数

```cpp
class MyTime
{
    //...
    friend MyTime operator+(int m, const MyTime & t)
    {
        return t + m;
    }
}
```

另一个写法，因为它不是类的member，所以不需要加`MyTime::`在函数名之前。

```cpp
class MyTime
{
    //...
    friend MyTime operator+(int m, const MyTime & t);
}
MyTime operator+(int m, const MyTime & t)
{
    return t + m;
}
```

友元函数的另一个应用范围是重载运算符`<<`和`>>`. 方法是一样的，这里不在赘述。需要注意的是，`<<`和`>>`都是表达式 (expression), 所以需要有返回值，并且返回值必须要分别是`std::cout`和`std::cin`以便于链式操作。

## 类型转换运算符`()`

类型转换运算符是一种特殊的运算符，它的定义不需要写返回值和输入参数即类型。如果在前面加上`explicit`关键词，则类型转换只能显示进行，如果出现隐式则会出现编译错误。

```cpp
//implicit conversion
operator int() const
{
    std::cout << "operator int()" << std::endl;
    return this->hours * 60 + this->minutes;
}
//explicit conversion, C++11 standard
explicit operator float() const
{
    std::cout << "explicit operator float()" << std::endl;
    return float(this->hours * 60 + this->minutes);
}
```

如果需要把一个基本数据类型或者别的对象转化为我们自定义的类，有两种办法：

- 利用constructor重载；
- 重载赋值运算符`=`.

这两个办法的写法利用之前所学的都可以知晓，需要注意的是，constructor的一种写法是

```cpp
MyTime t1 = 70;
```

这里的`=`并非是重载赋值运算符，而只是我们利用构造函数初始化`t1`的一个写法而已，它与

```cpp
MyTime t1(70);
MyTime t1 = MyTime(70);
```

这两种初始化的写法是等价的。

## *运算符`++`的重载

前置运算和后置运算`++`我们都可以重载。如果是重载前置运算符，则按照常理如下：

```cpp
// prefix increment
MyTime& operator++()
{
    this->minutes++;
    this->hours += this->minutes / 60;
    this->minutes = this->minutes % 60;
    return *this; 
}
```

如果重载后置运算符，则需要加一个`int`关键词：

```cpp
// postfix increment
MyTime operator++(int)
{
    MyTime old = *this; // keep the old value
    operator++();  // prefix increment
    return old; 
}
```

可以看到，因为前置运算符返回的是修改后的值，因此可以返回引用类型；而后置运算符返回的是修改前的值，因此不能返回应用类型（因为此时返回的是局部变量）。这一段的解释和本节的重点`class`无关，只和`function`有关。

## Operator `=` overloading and default copy assignment

赋值运算符同样可以重载。但如果我们没有它重载的代码，编译器也会自动生成一个它的重载的实现，逻辑是将赋值对象的所有非`static`成员变量的值赋给被赋值的对象。注意它和拷贝构造函数的区别：

```cpp
MyTime t1(1,59);
MyTime t2 = t1; // copy constructor
t2 = t1; // copy assignment
```

## Based and Derived `class`（父子类）

一个父类可以是一个原生的类（所有我们之前所讨论的），也可以是一个子类。一个子类通过继承可以拥有父类的成员变量和函数。我们的父类定义如下：

```cpp
class Base
{
  public:
    int a;
    int b;
    Base(int a = 0, int b = 0)
    {
        this->a = a;
        this->b = b;
        cout << "Constructor Base::Base(" << a << ", " << b << ")" << endl;
    }
    ~Base()
    {
        cout << "Destructor Base::~Base()" << endl;
    }
    int product()
    {
        return a * b;
    }
    friend std::ostream & operator<<(std::ostream & os, const Base & obj)
    {
        os << "Base: a = " << obj.a << ", b = " << obj.b;
        return os;
    }
};
```

我们的通过`: public Base`语句，让`Derived`类继承了`Base`类的成员变量和成员函数。

```cpp
class Derived: public Base
{
  public:
    int c;
    Derived(int c): Base(c - 2, c - 1), c(c)
    {
        this->a += 3; //it can be changed after initialization
        cout << "Constructor Derived::Derived(" << c << ")" << endl;
    }
    ~Derived()
    {
        cout << "Destructor Derived::~Derived()" << endl;
    }
    int product()
    {
        return Base::product() * c;
    }
    friend std::ostream & operator<<(std::ostream & os, const Derived & obj)
    {
        // call the friend function in Base class
        os << static_cast<const Base&>(obj) << endl;

        os << "Derived: c = " << obj.c;
        return os;
    }
};

```
需要注意的是：

- 子类可以拥有和父类同名的函数（如果加上类的名字，则不同）；
- 在一个子类对象创建的时候，程序会先调用父类的构造函数，因为子类的构造是依赖于父类的；在子类对象被销毁时，程序会先调用子类的析构函数，释放子类的信息，然后再调用父类的析构函数，释放父类的信息。从内存的角度理解，一个子类对象的前面一部分就是和父类的对象时一模一样的。因此创建时先创建前面父类的内容，再添加子类的内容；销毁时则相反。
- 由于父子类在内存中的排列，对于`Derived d`类型转换`static_cast<Base>(d)`是合法的。


## Access Control in `class`

### members

`private`（私有的）成员只可以在类内，或者类的`friend`朋友函数或类访问；而`public`（公有的）成员可以在任何地方使用；`protected`(被保护的)成员的权限介于`private`和`public`之间，可以在子类中被访问。

```cpp
class Base 
{
  protected:
    int n;
  private:
    void foo1(Base& b)
    {
        n++;    // Okay
        b.n++;  // Okay
    }
};
 
class Derived : public Base 
{
    void foo2(Base& b, Derived& d) 
    {
        n++;        //Okay
        this->n++;  //Okay
        //b.n++;      //Error. You cannot access a protected member through base
        d.n++;      //Okay
    }
};
void compare(Base& b, Derived& d) // a non-member non-friend function
{
    // b.n++; // Error
    // d.n++; // Error
}
```

对于`b.n++`编译错误的原因，我的理解是在子类的函数中不可以以下犯上修改父类的值。

### inheritance

- `public` 继承会保留父类成员的类型
- `protected`继承中父类里面`public`和`protected`成员会被转为`protected`成员; 当然`private`成员仍然是`private`.
- `private`继承会把所有成员都会变成`private`.


到此为止，CPP的`class`的特性就基本介绍完成了；除了基本的特性之外，CPP还提供了模版类，它的使用和模版函数类似，并没有什么特别的语法，在此不再赘述。

