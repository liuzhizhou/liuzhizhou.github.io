---
title: "C/C++ Lecture Notes 4"
date: 2023-03-08T18:49:21+08:00
Description: ""
Tags: ['array','string','structure','union','enum','typedef']
Categories: ['Codes','C/C++']
series:  ['series-cpplecture']
DisableComments: false
---

## Arrays


Array is a **contiguously allocated memory**. Its element type can be any fundamental type, such as `int`, `float` and `structure`, `class`, `point`, `enumeration`.

```cpp
int num_array1[5]; //uninitialized array, random values 
int num_array2[5] = {0, 1, 2, 3, 4}; //initialization
```

The length of an array could be a variable.

```cpp
int len = 1;
while ( len < 10 )
{
    int num_array2[len]; //variable-length array
    cout << "len = " << len;
    cout << “, sizeof(num_array2)) = ” //sizeof 的单位是？ Int32 = 4 B
            << sizeof(num_array2) << endl;
    len ++;
}
```

The number can be omitted.

```cpp
int num_array[ ] = {1, 2, 3, 4}; // the type of num_array is "array of 4 int”
```

It can be the argument of a function, but we must tell the length.

```cpp
float array_sum(float values[], size_t length);
float array_sum(float *values, size_t length);
// 他们exactly the same
```

There are no bounds-checking in C/C++. Therefore we can visit other memory by `array[-1]` or `array[N]`, where N is a number out of the range. Remember that **Arrays can be regarded as addresses, not objects.**

</font color=#FF0000> Multi-Arrays of unknown bound would cause an error. </font> (seems to be correlated with the concepts of pointers.)

`const` array can be used as function arguments to ensure (protect the array) the array's value has not change.

## Strings

### Array-style Strings

The string is in fact an array of characters (`char[3]`) and its length is to the first 0 or '\0' character.

```cpp
//Copy
char* strcpy( char* dest, const char* src );
//Safer one:
char *strncpy(char *dest, const char *src, size_t count);
// Concatenate: appends a copy of src to dest
char *strcat( char *dest, const char *src );
//Compare
int strcmp( const char *lhs, const char *rhs );
```

### `string` Class

```cpp
std::string str1 = "Hello";
std::string str2 = "SUSTech";
std::string result = str1 + ", " + str2;// “+” operation overloading
```

## Structures: `struct`

```cpp
struct Student{
    char name[4];
    int born;
    bool male; 
};

struct Student stu;
strcpy(stu.name, "Yu");
stu.born = 2000;
stu.male = true;

struct Student stu = {"Yu", 2000, true};

struct Student students[100];
students[50].born = 2002; 
```

Every type in the struct would occupy some memory. The computer would read memory 4 at a time therefore if their memory is as 4+4+1 then it becomes 4+4+4; if 2+1+4 it becomes 4+4; etc.

## `union`

Similar to struct but share the memory.

## `enum`

An example:

```cpp
enum datatype {TYPE_INT8=1, TYPE_INT16=2, TYPE_INT32=4, TYPE_INT64=8};
```

```cpp
struct Point{
    enum datatype type;
    union {
        std::int8_t data8[3];
        std::int16_t data16[3];
        std::int32_t data32[3];
        std::int64_t data64[3];
    };
};
size_t datawidth(struct Point pt)
{
    return size_t(pt.type) * 3;
}
```

```cpp
int64_t l1norm(struct Point pt)
{
  int64_t result = 0;
  switch(pt.type)
  {
    case (TYPE_INT8): 
      result = abs(pt.data8[0]) +
               abs(pt.data8[1]) +
               abs(pt.data8[2]);
       break;
    ...
```

## `typedef`

```cpp
typedef int myint;

typedef unsigned char vec3b[3];

typedef struct _rgb_struct{//name _rgb_struct can be omit
    unsigned char r;
    unsigned char g;
    unsigned char b;
} rgb_struct;
```

```cpp
myint num = 32;
unsigned char color[3];
vec3b color = {255, 0, 255}; 

rgb_struct rgb = {0, 255, 128};
```

Typical usage:

```cpp
#ifndef _UINT8_T
#define _UINT8_T
typedef unsigned char uint8_t;
#endif /* _UINT8_T */
```

```cpp
#if defined(_LP64) 
typedef int wchar_t; 
#else 
typedef long wchar_t; 
#endif
```

## Makefile

```shell
# ## VERSION 1
# hello: main.cpp printhello.cpp  factorial.cpp
# 	g++ -o hello main.cpp printhello.cpp  factorial.cpp

# ## VERSION 2
# CXX = g++
# TARGET = hello
# OBJ = main.o printhello.o factorial.o

# $(TARGET): $(OBJ)
# 	$(CXX) -o $(TARGET) $(OBJ)

# main.o: main.cpp
# 	$(CXX) -c main.cpp

# printhello.o: printhello.cpp
# 	$(CXX) -c printhello.cpp

# factorial.o: factorial.cpp
# 	$(CXX) -c factorial.cpp


# ## VERSION 3
# CXX = g++
# TARGET = hello
# OBJ = main.o printhello.o factorial.o

# CXXFLAGS = -c -Wall

# $(TARGET): $(OBJ)
# 	$(CXX) -o $@ $^

# %.o: %.cpp
# 	$(CXX) $(CXXFLAGS) $< -o $@

# .PHONY: clean
# clean:
# 	rm -f *.o $(TARGET)


## VERSION 4
CXX = g++
TARGET = hello
SRC = $(wildcard *.cpp)
OBJ = $(patsubst %.cpp, %.o, $(SRC))

CXXFLAGS = -c -Wall

$(TARGET): $(OBJ)
	$(CXX) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

.PHONY: clean
clean:
	rm -f *.o $(TARGET)
```