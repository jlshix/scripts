# 将 github 项目的 md 文件发表为 hexo 文章

## 概述

为自己的项目写的说明文件一般我也会直接发布到个人的博客中,

我的[个人博客](http://leoshi.me)使用的是 [hexo](https://hexo.io/zh-cn/),
托管在[github pages](https://github.com/jlshix/jlshix.github.io),
虽然功能简单但也够用, 且不用操心.

自己常用的电脑有好几台, 所以发布源就放在都能访问的服务器上了,
所以在发布的时候步骤比较繁杂:

- 将文件上传到服务器
- `hexo new filename`
- 复制与更改
- `hexo g` 生成
- `hexo s` 运行服务器进行预览
- 满意后使用 `hexo d` 部署

所以想要写脚本直接拉取已经发布到 github 上的 README 文件,
经过修改后直接发布到博客上.


## 设计

1. 输入
    - 一个来自本地或 github 的 md 文件
    - date (可选, 默认当前)
    - tags (列表, 至少一个)
    - categories (列表, 至少一个)

2. 处理过程
    - 获取文件
        - 本地文件则复制到目录
        - github 文件则下载到目录
    - 添加文件头
        - title 直接取一级标题, 并在正文中删除
        - date 默认或来自参数
        - tags 来自参数
        - categories 来自参数
    - 保存文件
    - 生成, 预览, 部署
    - 提交


## 实现

### 参数获取

关于命令行参数获取, 使用的是 `getopt`, 虽然比不用强得多, 但用起来也不是很舒服,
因为不支持位置参数和子命令, 所以只好把文件路径放在最后了.

写完之后, 发现应该用 `argparse`, 参考:

1. [python howto](https://docs.python.org/3/howto/argparse.html)
2. [getopt or argparse](https://ttboj.wordpress.com/2010/02/03/getopt-vs-optparse-vs-argparse/)


### 多行字符串处理

hexo 文章头是有确定的格式的, 在脚本中以模板呈现时要么行前空格过多, 要么对齐太难看,
所以使用 `textwraper.dedent` 处理这个问题, 可以自动以首行的缩进量对所有行进行处理.

其实整个文件生成过程完全可以用模板引擎(如 jinja 或 Mako)处理, 不过是不是有点小题大做了?


### 其它

整个实现逻辑和使用方式写在注释了, 格式什么的还有待改进,
功能比较简单, 通过阅读代码就可以弄懂.


## 总结

总体来讲有了这个脚本就可以节省一些发表文章的功夫了.

TODO:
- 文档与注释规范
- `argparse` 参数处理
- 更清晰的程序逻辑 

本程序的源码在 [Github](https://github.com/jlshix/scripts/blob/master/post_readme/postmd.py), 欢迎交流.
