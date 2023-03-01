---
title: "C/C++ Lecture Notes 2"
date: 2023-03-01T21:53:22+08:00
Description: ""
Tags: ['if else','for/while loop','goto & switch','Linux commands']
Categories: ['Codes','C/C++']
series:  ['series-cpplecture']
DisableComments: false
---

## `If` Statement

```cpp
if (condition)
{
    sth
}
// The following codes are equivalent

bool isPositive = true;
int factor = 0;
//some operations may change isPositive's value
if(isPositive)
    factor = 1;
else
    factor = -1;

// and

factor = isPositive ? 1 : -1;
// ? combined with : means
// If the thing in the front of ? is true, then (sth); 
// otherwise : (sth).
```

Moreover, we can write as 

```cpp
factor = (isPositive) * 2 - 1; 
```

This is faster than the above two.

The condition should be an expression (we would explain the meaning of expression later) which can be converted to bool. For example, an integer or float is true when it is not zero. <font color=#FF0000> Pointers are also frequently used condition.</font> (This would be explained in the future)

## `for/ while` Loop

```cpp
while( expression )
{
    //...
}

for (init-clause; cond-expression; iteration-expression)
{
    // loop-statement
}
```

`break` and `continue` are correspond to the nearest while or for. `break` means go to the end of the loop and `continue` means go back to the start of the loop.

Be careful that `a = 10` can be viewed as a expression that can be converted to bool.

We should also understand `do... while`, which is similar to `while`.

`for` can be stated without condition:

```cpp
for(;;) 
{
    // some statements
    cout << "endless loop!" << endl;
}

while(true)
{
    // some statements
    cout << "endless loop!" << endl;
}

// They are the same
```

## `goto` and `switch`

`goto` can help you jump to the desired location, but it is an unrecommended statement.

The following usage is OK:

```cpp
float mysquare(float value)
{
    float result = 0.0f;
    if(value >= 1.0f || value <= 0)
    {
        cerr << "The input is out of range." << endl;
        goto EXIT_ERROR;
    }
    result = value * value;
    return result;
    EXIT_ERROR:
    //do sth such as closing files here
    return 0.0f;
}
```

`switch` is more similar to `goto` than `if else`. Therefore we need a `break`! Do not forget it.

```cpp
switch (input_char)
{
    case 'a':
    case 'A':
        cout << "Move left." << endl;
        break;
    case 'd':
    case 'D':
        cout << "Move right." << endl;
        break;
    default: 
        cout << "Undefined key." << endl;
        break;
}
```

## Commands in Linux

My laptop is mac, but they are similar.

Directory means '文件夹' in Chinese.

`pwd`: Print the name of Working Directory.
`cd <directory name>`: Change the current Directory.
`ls`: List of content of current directory.
`mkdir <directory name>`: Make a new directory.
`rmdir <directory name>`: Remove empty directories.
`cat <file name>`: Display Content of the file.
`rm <file name>`: Remove a file (delete).
`cp <source> <dest>`: Copy.
`mv <source> <dest>`: Move a file.

Also, we can use `man <cmds>` to see how to use it. `where` is find the definition file of a command.

The website: https://www.javatpoint.com/linux-commands is useful.
