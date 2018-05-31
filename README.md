# Python爬虫汇总

这里我整理了一些我从学习写Python爬虫以来做的一些勉强拿的出手的项目，会伴随一些简单的介绍。我会从最新的开始整理，因此如果你发现代码的质量越来越差……相信我，学习是个衍变的过程。

每个项目我都同步写过文档，一并附上。

## 爬取动漫屋

博客文档: [爬取动漫屋](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-dong-man-wu)。

关键词：Python 3.6, requests, re, BeautifulSoup, 用js混淆js

爬取搜索页面下所有的漫画，以图片形式保存到本地。（实现核心代码）



## 分布式爬虫抓取空气质量指数

博客文档: [使用celery构建分布式爬虫抓取空气质量指数](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-kong-qi-zhi-liang-he-fen-bu-shi) 

关键词：Python 3.6, celery, BeautifulSoup, re, requests

使用celery消息队列实现空气质量指数的分布式爬取。



## 抓取空气质量指数

博客文档: [使用协程抓取空气质量指数](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-kong-qi-zhi-liang-he-xie-cheng) 

关键词：Python 3.6, 协程, BeautifulSoup, re, aiohttp, asyncio



## 使用Python获取天气信息

[博客文档: 使用Python获取天气信息](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-tian-qi) 

关键词：Python 3.6，requests, BeautifulSoup, re, sqlite3, ast



## 使用Python获取12306余票信息和票价

博客文档: [使用Python获取12306余票信息和票价](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-12306che-piao-huo-qu) 

关键词：Python 3.6, requests, json, sqlite3, prettytalbe, colorama



## 爬虫之刺 - 验证码

博客文档: 

- [Python爬虫之刺-验证码 - 简介](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-byan-zheng-ma-0)
- [Python爬虫之刺-字符验证码](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-byan-zheng-ma-1-zi-fu-yan-zheng-ma)
- Python爬虫之刺-字符验证码之去除干扰线
- [Python爬虫之刺-字符验证码之字符分割](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-byan-zheng-ma-3-zi-fu-fen-ge) 
- [Python爬虫之刺-字符验证码之倾斜矫正](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-byan-zheng-ma-4-qing-xie-jiao-zheng) 
- [Python爬虫之刺-字符验证码之样本训练](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-byan-zheng-ma-5-xun-lian-ji)
- [Python爬虫之刺-滑动验证码](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-byan-zheng-ma-6-hua-dong-yan-zheng-ma) 
- Python爬虫之刺-计算验证码
- Python爬虫之刺-识图验证码

关键词：tesserocr, numpy, PIL, matplotlib, claptcha, cv2

这是研究验证码时的所记录的笔记，算是一个系列的。大多数涉及到的代码我都自己写了，比如说：灰度二值化、连通图、字符分割、倾斜校正、样本训练等，没实现的有滴水算法，去除干扰线（确切地说是能成功去除干扰线的算法，我写了一个利用连通域去除干扰先的算法，但是用起来效果都不怎么样）。样本训练我也做了，但是个人觉得有点不属于爬虫的范畴了，比如识图验证码，更多的可能是利用学习算法构建训练样本，因此就没有继续深入下去。

滑动验证码会在下文淘宝项目里仔细解释。

## 微博

博客文档: 

[攻克微博(1) - 模拟微博登陆](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-wei-bo-1) 

[攻克微博(2) - 抓取关注和个人信息](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-wei-bo-2) 

关键词：Python 3.6, requests, re, RSA, base64, URLencode, bloomfilter, sqlite3

分析微博的登陆方式，模拟计算登陆请求所需要的参数，登陆成功获取Cookie。使用Cookie抓取微博用户的关注组和个人信息。预留抓取其他页面的接口，当时因为各种页面的抓取代码类似，没有全部实现。

## 斗鱼视频

博客文档: [斗鱼视频下载](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-dou-yu-shi-pin-xia-zai) 

关键词：Python 3.6, requests, re, progressbar

模拟手机请求，获取斗鱼视频碎片，下载并合并成完整视频。



## 二维码

博客文档: [码中码之图片之二维码](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-er-wei-ma) 

关键词：Python 3.6, PIL, qrcode

实现了两个功能：

1. 将一个图片分割成九等份，满足强迫症发布朋友圈。
2. 将二维码图片打印在命令行



## 爬取搜狗微信文章和公众号文章

博客文档: [爬取搜狗微信文章和公众号文章](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-wei-xin-wen-zhang) 

关键词：Python 3.6, requests, BeautifulSoup, tomd

模拟搜狗搜索的微信文章请求，抓取请求的页面并转化为md文件保存到本地。也是这个项目让我萌生了自己写一个HTML转MD的库。



## 淘宝

博客文档: 

[模拟淘宝登陆获取初始Cookie](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-mo-ni-deng-lu-tao-bao-.md) 

[淘宝抓取所有订单](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-tao-bao-huo-qu-suo-you-ding-dan) 

关键词：Python 3.6, requests, re, json, BeautifulSoup, PrettyTable, selenium, PhantomJS

实现账号密码和扫码两种登陆方式。其中账号密码登陆需要一个更可靠的鼠标轨迹模拟算法来通过极验的滑动验证码（非代码逻辑问题）。

登陆成功后获取Cookie，抓取我的订单页面下的所有历史订单。





## 百度贴吧

博客文档: [爬取百度某贴吧的精品贴](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-bai-du-tie-ba) 

关键词：Python 3.6, requests, re, json, BeautifulSoup

如题。代码中爬取的是复仇者联盟吧所有的精品贴，保存为本地txt文件。



## 虾米音乐

博客文档: [虾米音乐下载](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-xia-mi-yin-le-xia-zai) 

关键词：Python 3.6, requests, re, json, execjs

通过模拟请求获取音乐的下载地址，通过execjs执行js文件获取音乐文件的真实地址，下载音乐到本地。



## 网易云音乐

博客文档: [爬取网易云音乐我喜欢的音乐和热评](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-wang-yi-yun-re-ping) 

关键词：Python 3.6, requests, re, json, PrettyTable, sqlite3



## 今日头条

博客文档: [分析Ajax请求并抓取今日头条数据](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-jin-ri-tou-tiao) 

关键词：Python 3.6, requests, json, re

抓取今日头条的搜索页面，模拟XHR请求获取所有的搜索结果（两种，图库或文章）并将所有图片保存到本地。



## 猫眼电影TOP100

博客文档: [使用Requests+正则表达式爬取猫眼电影TOP100](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-mao-yan-dian-ying) 

关键词：Python 3.6, requests, re, json

如题。



## 糗事百科

博客文档: [爬取糗事百科的内容和图片并展示](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-qiu-shi-bai-ke) 

关键词：Python 3.6, urllib, hashlib, BeautifulSoup, tkinter, PIL

相当于一个离线糗百阅读器，除了丑陋一点以外。



## 爬取豆瓣Top250电影和灌篮高手漫画全集

博客文档: [Scrapy - 爬取豆瓣Top250电影和灌篮高手漫画全集](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-pa-chong-shi-li-2) 

这个当时还是个菜鸡，是照着别人的项目做的，主要学习了爬虫的基本抓取过程和scrapy的原理及其使用。



## 第一个爬虫和我的博客

博客文档: [第一个爬虫和我的博客](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-pa-chong-shi-li) 

第一个爬虫，纪念一下。



## 附赠 - 用Python向Kindle推送电子书

博客文档: [用Python向Kindle推送电子书](https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-kindledian-zi-shu-tui-song) 

关键词：Python 3.6, tkinter, smtp, pinyin

一个图形程序，功能如题。