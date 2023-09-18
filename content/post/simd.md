---
title:    "Single instruction, multiple data (SIMD)"
date:     2023-06-03T14:05:04+08:00
summary:  "A common way to speed up your program on a particular platform: just an introduction."
tags:     ['C and CPP', 'C and CPP-speed up']
draft:    false
---

正如SIMD的全称所表述的那样，它加快程序运行速度的办法是同时操作多个数据。如下图所示：

![simd](https://liuzhizhou.github.io/img/speed/simd.jpg)

假设图中的数据类型是`float`，那么图中左边的`+`就是常规`float`类型之间的加法，而图中右边的`+`则是SIMD的`+`operator. 此时，右侧方法的输出是两个`float32x4`(表示一个由4个大小为`float32`类型组成的类型)的数据，大小为`128`位(bits). 这个数据是会被存储在寄存器上。寄存器的大小由不同CPU而异。

常用的Intel CPU根据寄存器大小的区别，可以通过指令集SSE2(128bits), AVX2(256bits), AVX512(512bits)控制, 括号内是指令集对应的寄存器大小； ARM平台的CPU的SIMD指令集为NEON, 它的寄存器大小都是128bits.

根据上述信息我们可以知道，在不同平台上使用SIMD需要不同的指令才能实现。因此，如果你想让你的代码在不同平台上都通过SIMD加速，需要写不同的代码。所以SIMD是比较难维护的。一个解决方案是OpenCV给出的。它实现了一个universal intrinsics的指令集，使其能做所有平台上运行。我们可以通过这个指令集来完成，不过代价是必须引入OpenCV这个库。

下面，我们以`dotProduct`为例来看SIMD是如何实现的。

```cpp 
// "dotProductSIMD.hpp"
#pragma once

float dotproduct(const float *p1, const float * p2, size_t n);
float dotproduct_unloop(const float *p1, const float * p2, size_t n);
float dotproduct_avx2(const float *p1, const float * p2, size_t n);
float dotproduct_neon(const float *p1, const float * p2, size_t n);
```

这里我们定义的`dotproduct()`是常规的，`dotproduct_unloop()`对循环的次数进行了优化（由于每次循环之前涉及一次判断，因此循环次数越少，速度应该越快），`dotproduct_avx2()`是SIMD，基于Intel CPU的AVX2指令集，`dotproduct_neon()`也是SIMD，但是基于ARM的NEON指令集。

```cpp
// "dotProductSIMD.cpp"

#include <iostream>
#include "dotProductSIMD.hpp"

#ifdef WITH_AVX2
#include <immintrin.h>
#endif 

#ifdef WITH_NEON
#include <arm_neon.h>
#endif


float dotproduct(const float *p1, const float * p2, size_t n)
{
    float sum = 0.0f;
    for (size_t i = 0; i < n ; i++)
        sum += (p1[i] * p2[i]);
    return sum;
}


float dotproduct_unloop(const float *p1, const float * p2, size_t n)
{
    if(n % 8 != 0)
    {
        std::cerr << "The size n must be a multiple of 8." <<std::endl;
        return 0.0f;
    }

    float sum = 0.0f;
    for (size_t i = 0; i < n; i+=8)
    {
        sum += (p1[i] * p2[i]);
        sum += (p1[i+1] * p2[i+1]);
        sum += (p1[i+2] * p2[i+2]);
        sum += (p1[i+3] * p2[i+3]);
        sum += (p1[i+4] * p2[i+4]);
        sum += (p1[i+5] * p2[i+5]);
        sum += (p1[i+6] * p2[i+6]);
        sum += (p1[i+7] * p2[i+7]);
    }
    return sum;

}

float dotproduct_avx2(const float *p1, const float * p2, size_t n)
{
#ifdef WITH_AVX2
    if(n % 8 != 0)
    {
        std::cerr << "The size n must be a multiple of 8." <<std::endl;
        return 0.0f;
    }

    float sum[8] = {0};
    __m256 a, b;
    __m256 c = _mm256_setzero_ps();

    for (size_t i = 0; i < n; i+=8)
    {
        a = _mm256_loadu_ps(p1 + i);
        b = _mm256_loadu_ps(p2 + i);
        c =  _mm256_add_ps(c, _mm256_mul_ps(a, b));
    }
    _mm256_storeu_ps(sum, c);
    return (sum[0]+sum[1]+sum[2]+sum[3]+sum[4]+sum[5]+sum[6]+sum[7]);
#else
    std::cerr << "AVX2 is not supported" << std::endl;
    return 0.0;
#endif
}


float dotproduct_neon(const float *p1, const float * p2, size_t n)
{
#ifdef WITH_NEON
    if(n % 4 != 0)
    {
        std::cerr << "The size n must be a multiple of 4." <<std::endl;
        return 0.0f;
    }

    float sum[4] = {0};
    float32x4_t a, b;
    float32x4_t c = vdupq_n_f32(0);

    for (size_t i = 0; i < n; i+=4)
    {
        a = vld1q_f32(p1 + i);
        b = vld1q_f32(p2 + i);
        c =  vaddq_f32(c, vmulq_f32(a, b));
    }
    vst1q_f32(sum, c);
    return (sum[0]+sum[1]+sum[2]+sum[3]);
#else
    std::cerr << "NEON is not supported" << std::endl;
    return 0.0;
#endif
}
```

如果对程序进行测速，那么在Intel 256位寄存器之下，我们应该能够获得$256\div32=8$倍提速; 在NEON 128位寄存器下，我们应该得到$4$倍提速。而单纯的减少循环次数并不会提速（尽管理论上会），这是因为我们的编译器非常聪明，会对原本最简单`dotproduct()`函数进行基础的优化。

需要注意的是，在使用SIMD时，需要使用类似

```cpp
// 256bits aligned, C++17 standard
static_cast<float*>(aligned_alloc(256, nSize*sizeof(float))); 
```

语句对内存进行对齐，否则无法正常运行（原因？）。

这就是对于SIMD的简单介绍，例子中的代码来源于[GitHub - 于仕琪老师的Repo: CPP](https://github.com/ShiqiYu/CPP/tree/main/week08/examples)，也是我学习C/CPP的场所。视频讲解参见[Bilibili - 于仕琪老师的C/C++从基础语法到优化策略课程](https://www.bilibili.com/video/BV1Vf4y1P7pq/?spm_id_from=333.999.0.0)第8.2, 8.3节。

有用的链接：

- Intel的SIMD指令集的官方网站: https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html
- ARM的SIMD指令集NEON得官方网站：https://developer.arm.com/architectures/instruction-sets/intrinsics/ 
- 于仕琪老师的开源项目libfacedetection(基于CPP，不依赖于任何库，甚至数学库)，里面有很多函数都使用了SIMD进行全平台优化: https://github.com/ShiqiYu/libfacedetection


