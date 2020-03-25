# 简单脚本下载动漫之家一拳超人漫画


最近入手了一个 kindle 乞丐版. 读书和盖泡面(误)之外, 想来也是绝佳的漫画神器.

硬件有了, 找资源成了问题, 找来找去只有在线看或者下载 APP,
这样一看我一直以来看漫画的方式也是如此.

只好自己动手丰衣足食了.

想想现在还在追的漫画, 就只有一拳超人和海贼王了.
一拳超人一直在动漫之家看, 海贼王在鼠绘.

以前者为例, 简单说一下下载过程.

## 设计

浏览器打开[一拳超人漫画主页](https://manhua.dmzj.com/yiquanchaoren),
可以看到各个章节已经展现在所有的页面上, 我们要做的事情是:

1. 提取所有的章节名称和链接, 前者用于建立文件夹, 后者用于访问
2. 对于任一章节, 提取所有图片的链接
3. 根据链接下载图片

## 工具

作为一棵对爬虫几乎一无所知的菜, 平常能用到的就只有 requests 和 BeautifulSoup 这两个库了,
这一次的情况还不至于动用爬虫框架, 另外多线程也没用, 一是反反爬比较麻烦, 二是网站也要恰饭的嘛, 毕竟不是正规方式.

以下是这两个神器的官方文档:
 - [requests](http://docs.python-requests.org/zh_CN/latest/index.html)
 - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html)

 安装则使用 pip:
 - `pip install requests`
 - `pip install bs4`

## 实现

### 提取章节名称与链接

首先在任一章节名右键, 选择`检查`, 打开开发者工具, 可以看到其所在 div 的结构:
```html
<div class="cartoon_online_border" style="display:none">
    <ul>
        <li>
            <a title="一拳超人-特别篇" href="/yiquanchaoren/19842.shtml" >特别篇</a>
        </li>
        ...
    </ul>
</div>
```
另外还有 `<div class="cartoon_online_border_other" >` 存放了 ONE 老师的原作版以及其他版本,
内部结构也是一致的.

我们只要提取所有 `<a>` 标签的 `title` 和 `href` 属性即可, 后者需要与 `https://manhua.dmzj.com` 进行拼接
才是正确的章节地址.

```python
# 获取主页 html
req = requests.get(link, headers=headers)
# 解析
soup = BeautifulSoup(req.text, 'lxml')
# 存储结果
res = []

# 查找 div, 提取 ul -> li -> a 中的对应内容
for div in soup.find_all('div', class_='cartoon_online_border'):
    for li in div.ul:
        if type(li).__name__ == 'Tag':
            res.append((li.a['title'], domain + li.a['href']))
```


### 提取图片链接

这一步其实花了最多的时间, 主要是找链接到底存在哪里了.

众所周知, JS 的广泛使用为爬虫的工作带来了很大难度,
F12 打开开发者工具, 刷新页面, 在 Network 选项卡观察载入顺序, 可以看到
除了主页外载入的各种资源, 各个 JS 都是压缩后的, 难以阅读.

找了很久图片链接的位置, 后来发现生成链接的代码位置竟然藏在 html 的 script 块里.

以第 74 话为例, 可以看到:
```html
<script type="text/javascript">
    var arr_img = new Array();
    var page = '';
    eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('l k=k=\'["y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/2.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/3.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/4.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/5.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/6.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/7.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/8.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/9.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/q.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/o-n.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/m.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/p.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/t.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/w.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/r.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/x.f","y\\/%1%g%e%b%a%d%c%h%i%1%0%0\\/j\\/%b%a%v%s%a%u.f"]\';',35,35,'BA|E4|||||||||8B|E6|E8|B3|80|jpg|B8|B6|85|74|pages|var|13|12|11|14|10|17|E5|15|9F|9B|16|18|'.split('|'),0,{}));
    var g_comic_name = "一拳超人";
    var g_chapter_name = "第74话";
    var g_comic_url = "yiquanchaoren/";
    var g_chapter_url = "yiquanchaoren/38720.shtml";
    var g_current_page = 1;
    var g_max_pic_count = 17;
    var g_page_base = '';
    var g_comic_id = res_id = '9949';
    var g_chapter_id = chapter_id = '38720';
    var g_comic_code = '135d58b4af3a33b76cc76d21d317422e';
    var arr_pages = eval(pages);
    var next_chapter_pages = '["y\/%E4%B8%80%E6%8B%B3%E8%B6%85%E4%BA%BA\/75\/2.jpg","y\/%E4%B8%80%E6%8B%B3%E8%B6%85%E4%BA%BA\/75\/3.jpg","y\/%E4%B8%80%E6%8B%B3%E8%B6%85%E4%BA%BA\/75\/4.jpg"]';
    var arr_nextchapter_pages = eval(next_chapter_pages);
    var final_page_url = "/yiquanchaoren/jump.shtml?9949_38720&d8a250eed5aa18d31b1f95e0ed385f9d";
    var sns_sys_id = '9949_38720';
    var sns_view_point_token = 'd8a250eed5aa18d31b1f95e0ed385f9d';
    var is_hot_comic = false;
    var is_fast_comic = true;
    var server_name = 0;
    var page_site_root = '/';
    var res_type = 1;
</script>
```

这个时候 `arr_pages` 这个变量存储的就是所有的图片链接了, 真是意想不到的方法.

那么, 如何在不使用模拟浏览器的情况下执行 JS 代码呢?

答案是 `pyexecjs`, 使用 `pip install pyexecjs` 安装后即可使用.
执行代码也很简单, 例如:

```python
import execjs
execjs.eval("'red yellow blue'.split(' ')")
# ['red', 'yellow', 'blue']
```

对于万能的 JS, 我也是个菜, 经过多次尝试发现
对于我们现在的情况, 需要包装成带返回的函数形式, 代码如下:

```python
code = 'function(){' + soup.script.text + ' return arr_pages; }()'
head = 'https://images.dmzj.com/'
res = [head + x for x in execjs.eval(code)]
```

### 下载图片

拿到单个图片的链接, 我们就可以进行下载了:

```python
# 请求图片链接
req = requests.get(link, headers=headers)
# 生成保存路径
path = os.path.join(folder, link.split('/')[-1])
with open(path, 'wb') as f:
    f.write(req.content)
```

## 注意

1. 动漫之家的反爬虫措施很容易就摸清了, 只验证 `request headers` 中的 refer 字段.
也就是说在请求下载图片时只要附带所属的章节地址即可

2. 下载的漫画图片文件名是及其不规律的, 一开始是 `01, 02, 03...`, 后来村田老师出了上百页的一话
(如125话), 就会变成 `001, 002, 003...`, 也有不知为何使用了 `0001, 0002, 0003` 的章节.
最主要的问题是连页会命名为 `30-31, 32-33`, 就根本不是一般的数字了, 所以列举是行不通的.

3. python3 的编解码问题相对于 python2 来说可以几乎不用在意了, 但包含中文的网址在 chrome 地址栏的显示并不是
真实的网址文本. 在 python 中需要使用 `urllib.parse.unquote` 进行解码.
```python
>>> import urllib
>>> s = '%E4%B8%80%E6%8B%B3%E8%B6%85%E4%BA%BA'
>>> urllib.parse.unquote(s)
'一拳超人'
```

4. 仅使用单线程的话效率不高, 但也是对服务器最友好的方式(加了 sleep 就更友好了),
我这边的情况是, 在两小时内大约下载了 150 章.
对于多线程, 动漫之家那边应该也是有所防备的, 脚本下载的同时使用浏览器就无法访问了.
对于这个问题就只能使用代理了.

5. 没有进行错误处理, 出错就终止, 在 150 章的下载过程中狗带了三四次, 然后重新运行又会继续下载了,
不过需要将当前章节的文件夹删掉, 因为是检查文件夹来决定是否跳过的.

---

## 改进

上次的漫画爬虫爬取一拳超人, 在后期的工作中出错率越来越高了,
于是又进行了一些优化:

1. 抓取名称优化
2. GET 请求的超时与重试
4. 每章图片下载队列

至于单线程的问题, 是 feature, 体现了对动漫之家的尊重(大误).

另外本想试一下这个脚本是否可以下载动漫之家其他漫画, 后来发现想看的都下架了,
于是就鸽了(人类的本质...), 有兴趣可以自行探索, 欢迎交流.


### 抓取名称优化

首先是一个不起眼的优化, 更改了提取标题的逻辑.

对于每一话标题的 HTML, 如:
`<a title="一拳超人-第125话" href="/yiquanchaoren/67625.shtml">第125话</a>`

之前提取的是 `title` 和 `href` 属性, 在使用前者建立文件夹时使用的是 `title.split('-')[-1]` 作为文件夹名称

但在下载到原作版时, 例如:
`<a title="一拳超人-原作版20-23" href="/yiquanchaoren/20142.shtml">原作版20-23</a>`
就剩下一个 `23` 了, 所以直接提取 `a` 标签所包含的文本

即从 `li.a['title']` 改为 `li.a.text`


### GET 的超时与重试

GET 请求总是难以预料的, requests 的设计非常之优秀, 还只看了个皮毛就可以完成基本操作.

关于超时可以看 [官方文档关于超时的用法讲解](http://docs.python-requests.org/zh_CN/latest/user/advanced.html#timeout).

关于重试可以看 [StackOverflow 的这个问题](https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request).

用新增的 `ht_get(link, headers=headers)` 代替获取漫画章节列表和每章节获取图片列表时使用的 `requests.get` 即可,
默认重复请求 `max_retry` 次, 我这边的情况是一般一次成功, 最多两次.

其中 `timeout` 是一个二元组, 分别表示连接超时和读取超时.


### 每章图片下载队列

这是这一版本的最大改动, 基本逻辑是:
维护一个队列 `collections.deque`, 遍历图片列表下载失败后则存入下载参数和重复次数,
图片列表遍历完毕后开始处理队列:
队列不空的情况下:
- 出队下载
    - 成功下载
    - 下载失败则检查重试次数
        - 小于最大重试次数, 次数+1, 重新入队
        - 大于最大重试次数, 将下载参数写入log文件

这个行为推测和浏览器访问章节网页时的行为基本一致, 因此并未被网站的反爬虫策略发现,
我这边的情况是, 整个执行过程中未发生超过最大重试次数(5次)的情况.
