---
title:  "OpenMP"
date:   2023-06-03T16:44:44+08:00
summary: "An introduction to how to use OpenMP to speed up CPP program."
tags:     ['C and CPP', 'C and CPP-speed up']
draft:  false
---

假设我们已经知道了如何使用[SIMD](https://liuzhizhou.github.io/blog/simd/)优化代码。利用SIMD时，虽然我们可以同时操作多个数据，但我们本质上只使用了CPU的单个内核。我们的CPU通常都是多核的，如果只利用一个内核的话，那么我们肯定没有充分施展CPU的性能。我们这里介绍的OpenMP就提供了一个解决方案。它的使用非常简单，只需要先`#include <omp.h>`, 再在循环之前加入`#pragma omp parallel for`语句即可，即

```cpp
#include <omp.h>

#pragma omp parallel for
for (size_t i = 0; i < n; i++)
{
    //...
}
```

它的原理很简单，就是将一个$n$次循环根据内核的个数$k$, 拆分为对应的$k$个$n/k$次循环，每个内核分配一个。这样一来，理论上内核数量就是我们能够提升的性能；例如如果有8个内核，那么运算效率就可以提升8倍。

下面我们说一些使用时的注意事项。

- 如果涉及多层循环，那么我们最好在第一层循环外使用`#pragma omp parallel for`, 原因是因为这行语句的执行是需要代价的，因此拆分循环是需要一定计算的，我们希望每次拆分后所做的事情想对于这个代价越大越好，这样的话这个代价就会相对小，性能提升就会明显。
- 使用OpenMP时，如果涉及变量赋值，则需要非常小心。因为在并行计算时，同时写入同一个数据会造成写入冲突，从而影响最后的结果。例如我们直接对我们之前的例子(参见[SIMD](https://liuzhizhou.github.io/blog/simd/))`dotproduct_neon`进行修改：

```cpp
float dotproduct_neon_mp(const float *p1, const float * p2, size_t n)
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

    #pragma omp parallel for
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

此时就涉及到并行时对于`c`的写入冲突，因此不能这样使用。
