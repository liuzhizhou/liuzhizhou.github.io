---
title: "C/C++ Lecture Notes 1"
date: 2023-02-22T13:05:39+08:00
draft: false
series: 
    - series-cpplecture

tags :
    - compile
    - run
    - error
    - input & output


categories :
    - Codes
    - C/C++
---

Lecture notes and examples: https://github.com/ShiqiYu/CPP
Lecture videos: https://www.bilibili.com/video/BV1Vf4y1P7pq


## How C/C++ work?
Compile+link and run are two (three) seperated steps. Commonly we use `g++ -o` or just `g++` to compile and link together.

```shell
g++ hello.cpp # compile and link

g++ hello.cpp --std=c++11 # compile and link using c++v.11

g++ hello.cpp --std=c++11 -o hello # compile  and let the name of the output file be hello, the default name is a.out
```

Execute (run) the program

```shell
./hello # if the output file name is changed to hello. 

#Default: 
./a.out
```

We should seperate our scource codes in to multiple files to make it clear. For example, we want a `mul(a,b)` function. Then we have a file named "mul.cpp":

```cpp "mul.cpp"
int mul(int a, int b) // this sentence helps us know the functions we are defining or using.

int mul(int a, int b)
{
    return a*b
}
```

To make it more clear (another advantage is that we can use it in another .cpp documents), we seperate it into two files. 

The first is "mul.hpp", the head file.

```cpp
#progama once // Prevent head file to be compiled multiple times

int mul(int a, int b);
```

The second is "mul.cpp":

```cpp "mul.cpp"
int mul(int a, int b)
{
    return a*b
}
```

Now if we want to use this function in another file, say "main.cpp", we can write:

```cpp
#include <iostream> 
#include "mul.hpp"

using namespace std; 
int main()
{
    int a, b;
    int result;
    cout << "Pick two integers:"; 
    cin >> a;
    cin >> b;
    result = mul(a, b);
    cout << "The result is " << result << endl;
    return 0;
}
```

There is no need to write the disclaim part `int mul(int a, int b)` for twice.

However, "main.cpp" and "mul.cpp" are two files. How would the system know they are actually linked. It turns out that we should tell the system.

```shell
g++ -c main.cpp

g++ -c mul.cpp

# this step is called preprocess and compile
# the meaning of preprocess will be discussed later
# we do this to the two .cpp documents
# the system would generate two files
# main.o and mul.o

g++ main.o mul.o -o mainmul # output file is named as "mainmul" that can be executed

./mainmul # Run
```

Question: why the shell commands are different with the previous one, which is simply `g++ x.cpp -o`? (We didn't use `-c` there) This is because `-o` can automatically compile and link together, so that we can simply write in one line.

```shell
g++ main.cpp mul.cpp -o mainmul

./mainmul
```

If we do not care about the name of the executive file, we can further omit the `-o`, that is

```shell
g++ main.cpp mul.cpp

./a.out
```

## Errors

In different steps, we may face different errors. The steps are compiling, linking and running so we have compilation errors, link errors and runtime errors.

When we have compilation errors, normally it means there are some mistakes in grammar. We should check the grammar of source codes for this error. Link errors occur when we use a function that we do not define or misspelled. Runtime errors mean that the source codes are successfully compiled and linked, but some codes can not be implemented or we have a logic error.

## Preprocessor and Macros

In fact, there is another step before compilation, that is preprocessing. As we can see `# include` or something like that. `# include "mul.hpp"` means copy the line in "mul.hpp" and paste it to this file right here. `#define PI 3.14` means to change all `PI` in the codes to `3.14`. A problem in our quiz is the following:

```cpp
#define ADD2(n) n+2

int m = 3;

int n = ADD2(m) * 2;
```

I think the value of n should be 10 since $(3+2)\times 2=10$, but actually, the macro only subsitute the codes, so it would be $3+2 \times 2=7$.

## Simple Output and Input

The output code in C++ is like:

```cpp
cout << "hello." << endl;
```

<font color=#FF0000> Here, `cout` is an object of data type ostream in namespace std. (Just copy from the slides, I actually can't understand the words). `<<` is an operator (also don't understand) </font>

endl, an output-only I/O manipulator. It will output a new line character and flushes.

The input code in C++ is like:

```cpp
int a;
float b;
cin >> a;
cin >> b;
```

The output code in C is like:

```c
int v = 100;
printf("Hello, value = %d\n",v)
```

Here `int printf( const char *format, ... );` is a function.

The input code in C is like:

```c
int v;
int ret = scanf("%d", &v);
```

`scanf` reads data from stdin, and interpret the input as an integer and store it into v.