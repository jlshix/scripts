# 下载风之动漫海贼王漫画

## 列表页

打开风之动漫海贼王漫画列表页, [海贼王-风之动漫](https://manhua.fzdm.com/02//),
查看每一话的链接, 发现每一话都是在 `https://manhua.fzdm.com/02//` 之后加了序号,
如 975 话就是 `https://manhua.fzdm.com/02//975`.
所以我们无需抓取列表页就可以生成每一话的链接.


## 详情页

打开第 975 话, 右击图片选择在新标签页打开图片, 可以发现第一张漫画的地址是
`http://www-mipengine-org.mipcdn.com/i/p2.manhuapan.com/2020/03/20120019937512.jpg`,

查看网页源代码, 搜索 `20120019937512.jpg`, 有一处匹配:

```js
var Title="海贼王975话";var Clid="2";var mhurl="2020/03/20120019937512.jpg";var Url="975";var nexturl="";var CTitle="海贼王";var mhss=getCookie("picHost");if(mhss==""){mhss="p1.manhuapan.com"}if(mhurl.indexOf("2016")==-1&&mhurl.indexOf("2017")==-1&&mhurl.indexOf("2018")==-1&&mhurl.indexOf("2019")==-1&&mhurl.indexOf("2020")==-1){mhss="p2.manhuapan.com"}var mhpicurl=mhss+"/"+mhurl;if(mhurl.indexOf("http")!=-1){mhpicurl=mhurl}function nofind(){var e=new Date;e.setTime(e.getTime()-1);document.cookie="picHost=0;path=/;domain=fzdm.com;expires="+e.toGMTString();toastr.error("正在选择最快服务器ing～请不要本刷新页面。。。",{timeOut:1e3});testing();setTimeout("toastr.info('正在测试服务器中……请稍等', {timeOut: 800})",5e3);setTimeout("toastr.success('已为您切换最快服务器，请按f5刷新本页面！', {timeOut: 30000})",9e3)}  ;document.write('<img src="http://'+mhpicurl+'" width="0" height="0" referrerpolicy="no-referrer" />');  
```

可以发现图片地址是由 `http://www-mipengine-org.mipcdn.com/i/p2.manhuapan.com/` 和
`2020/03/20120019937512.jpg` 拼接而成的, 我们只要匹配每一页的这个部分即可.

点击网页上的下一页按钮跳转到第二页, 地址栏网址变为 `https://manhua.fzdm.com/02//975/index_1.html`,

再点上一页, 地址栏网址变为 `https://manhua.fzdm.com/02//975/index_0.html`,

可以得到出详情页每一页的地址规律.

每一页的结构是一样的, 可以使用同样的匹配规则得到图片的地址.

那么如何确定最后一页呢?

第 975 话共有 16 页, 最后一页的网址为 `https://manhua.fzdm.com/02//975/index_15.html`,

可以发现分页导航最后多出一条提示 "最后一页了", 我们可以通过判定网页源码中是否包含 "最后一页了"
来确定是否停止循环.


## 实现

首先我们定义一个函数 `get_episode(ep: int)`, 输入为某一话的编号, 根据此编号下载所有图片,
编号为 `01.jpg, 02.jpg, ...` 保存在名为 ep 的值的文件夹中.

`get_episode` 又调用两个函数:

1. `get_single(ep: int, i: int, retry: int = 5)`
根据话数 ep 和页数 i (从 0 开始) 获取单个网页的图片, 自带重试次数, 全部失败抛出异常.
返回元组, 第一个元素为 bool, 确认是否为最后一张, 第二个为 str, 为图片的完整网址.

2. `save_pic(url: str, name: str)`
根据 url 下载图片, 保存到 name 指定的路径中.


## 总结

综上, 实现了海贼王漫画的下载.

需要注意的是确定合适的请求间隔, 一方面为了我们自己不被反爬虫, 另一方面也为了网站本身的发展.

风之动漫的其他漫画没有尝试, 应该差不多.