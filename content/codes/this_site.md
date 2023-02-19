---
title: "本主页的搭建方法"
date: 2023-02-19T21:45:21+08:00
draft: false
---

如果你也需要/想要一个类似的个人博客，可以参考[这个网页](https://pingfan.me/posts/cs/create_blog_with_zero_experience/)和[这个Youtube视频](https://www.youtube.com/watch?v=dbtMf3kXUfw&t=754s)。超级友好地，利用[Hugo](Hugohttps://gohugo.io)和GitHub的Personal Page功能，实现了个人博客的需求。

其中有一些东西他没有讲，我补充在此：

1. 需要将brew添加到主环境变量中，不然关掉Termial就用不了了。方法是在Terminal中输入如下代码。


```
    echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.bash_profile 

    source ~/.bash_profile

    echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc   

    source ~/.zshrc
```

2. GitHub在Terminal中登入时，输入的是生成的Token，如果他提示密码已经过期了的话。在[这个CSDN的文章](https://blog.csdn.net/FatalFlower/article/details/119717823)里写的很清楚。
   
3. 如果把仓库名字设置成自己的id加.github.io的话，那么Personal Page的域名将会变成 your_id.github.io , 譬如我的话就是 liuzhizhou.github.io 这样更像一个个人主页一些，而不是项目主页。

还有更新仓库的代码，用的也很频繁，记录在此:
```
    git status 
    git add .
    git commit -m "msg"
    git push
```