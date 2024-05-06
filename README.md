# 如何使用？ 
## 一、更新记录

2024年3月22日23:47:22

网址签到sign参数逻辑调整，最新版已支持

2024年3月19日08:41:30

网址签到调整为表单添加sign参数的方式，最新版已支持

2024年3月13日22:57:21

网站签到调整为renji_***.js的验证逻辑，暂无解决方案，项目搁置

2024年3月4日21:35:56

网址签到添加了geetest极验的滑块验证，暂无解决方案，项目搁置

## 二、使用说明

1、Fork项目到自己的仓库

2、点击Settings -> 点击选项卡 Secrets and variables -> 点击Actions -> New repository secret

(1)目前预设3个，再多个的话，需要对应调整下代码，也很简单

因为考虑cookie中的特殊字符，暂时不考虑用字符拼接多个，再去py里切割的方案

(2)关于Bark推送，不用的话填空即可


    | Name   | Secret                           |
    | ------ | ------------------------------- |
    | COOKIE1  | 第一个Cookie |
    | COOKIE2  | 第二个Cookie |
    | COOKIE3  | 第三个Cookie |
    | BARK_DEVICEKEY  | IOS应用Bark 推送密钥 |
    | BARK_ICON  | IOS应用Bark 推送的图标 |

3、点击Actions -> 选择hifini-sign -> 点击Run workflow 运行即可

4、关于签到的定时时间

近期发现服务器会在后半夜维护，页面提示：维护中..请5:20以后访问

所以定时的时间尽量在这个后面，暂时不研究遇到维护情况自动后延签到的逻辑实现

hifinisign.yml，调整 \- cron: 20 21 * * *，对应北京时间5:20

5、参考仓库

感谢 https://github.com/Xramas/HiFiNi-Auto-Sign 提供思路

推荐 https://github.com/anduinnn/HiFiNi-Auto-CheckIn 此仓库在持续更新
