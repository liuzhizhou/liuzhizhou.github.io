---
title: "C/C++ Lecture Notes 2"
date: 2023-02-22T17:51:39+08:00
draft: false
series: 
    - series-cpplecture

tags :
    - data type
    - integer
    - float

categories :
    - Codes
    - C/C++
---


## Integer

Defining:

```cpp
int i = 10;

int j; // BAD
j = 10 
// This is called assignment
// Not Initialize
```

Remmber to initialize a variable althought it would not cause an error. C++ would initialize a  random number if you do not initialize it.

`int` has 32-bit but one bit for sign. So that its range is [-2^31, 2^31-1].

`unsigned int` does not have that bit for sign, its range is [0,2^32-1].

Normally, int is 32-bit but it is not always the case. We can use long int, short int or long long for different lower or higher bit. There number of bits are also not fixed. Commonly, short is 16 bit, long is 32 bit, long long is 64 bit.

![shortlongbit](/static/images/cpp_L2/shortlongbit.png)

We can use `sizeof()` to see the number of bit. Note that this is not a function but a operator since a function can not input `int` like `sizeof(int);sizeof(long int)`.

## More Integer

`char` is also a kind of integer. It can be viewed as `int8`. Sometimes `char` means `signed char` but sometimes it means `unsigned char`. Therefore we should specific sign or unsign when using it.

`bool` is also a kind of integer. Unexpectedly, it also have 8 bits not 1 bit. We can think 1 means true and not 1 means false. Normally we use 0 to mean false. Also `bool` is only in C++ but not in C. In C, we should define it if we want it.

```c
typedef char bool;
#define true 1
#define false 0
```

Or some one has do it for us

```c
#include <stdbool.h>
```

We have seen that the name would refer to different data types in different machine. So we can use the following instead. 

```
#include <cstdint>

int8_t
int16_t
int32_t
int64_t
uint8_t
uint16_t
uint32_t
uint64_t
...
```

`<cstdint>` also provides Macros:Some useful macros INT8_MIN, INT16_MIN, INT32_MIN, INT64_MIN,...

## Floating-Point Numbers

Constant numbers. 

```cpp
95 // decimal
0137 //octal
0x5F // hexademimal

95 //int
95u //unsigned int
95l //long
95ul //unsigned long
5.0 //double
5.f //float
```

The figure below illustrates how float (32-bit) works.

![float1](/static/images/cpp_L2/float1.png)
![float1](/static/images/cpp_L2/float2.png)

As a consequence, if a float number can be written as $\pm 2^n\times (1+2^{-m})$ for $0\leq n\leq 7$ and $0\leq m\leq 22$. Then it is precise.

Type `auto` is a type that would be determined when initialization. This is useful when we don't know the input type.

## Conversion

Use explicit conversion if possible (always)!

```cpp
int num_int1 = 9; // initializing an int value to num_int1
int num_int2 = 'C'; // implicit conversion
int num_int3 = (int)'C'; // explicit conversion, C-style
int num_int4 = int('C'); // explicit conversion, function style
int num_int5 = 2.8; //implicit conversion 2.8 是 double
float num_float = 2.3; //implicit conversion from double to float
short num_short = 650000; //ERROR
```

## Constant

```cpp
const float pi = 3.1415926f;
pi += 1; //error!
```
If a variable/object is const-qualified, it cannot be modified. 
It must be initialized when you define it.
