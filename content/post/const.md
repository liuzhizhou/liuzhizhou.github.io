---
title:  "Keyword `const` in C and CPP"
date:   2023-06-03T20:10:29+08:00
summary: A collection of usages of the keyword `const` in C and CPP.
tags:     ['C and CPP', 'const']
draft:  false
---


- In C language, one often use the macro way to define a constant number; in CPP, we often use `const` keyword.

```c
# define VALUE 100 //C style
const int value = 100; // CPP style
```

- A confusing part of `const` occurs with point.

```cpp
const int * p_int;
int const * p_int;

int * const p_int;
```

`const int *`means a pointer points to a `const int`; therefore the value of pointer points to cannot be changed. `int const *` means the same thing. While `int * const` means a `int *` pointer with `const` value, so that the real value (the address) of the pointer cannot be changed. 

In the input of a function, we sometimes use `const in` or `const int *` to make others to believe that this function will NOT change the value of place where the pointer points to.

```cpp
void func(const int *);
void func(const int &);
```

In a class, we may have `const` member and `const` function. A `const` member is just a member with `const` definition. A `const` function is a member function that cannot change the value of member variable. For example, the following codes should be a compilation error.

```cpp
class Student
{
private:
    const int BMI = 24;
    int born;
public:
    int getBorn() const
    {
        born++; //compilation error
        return born;
    }
}
```

