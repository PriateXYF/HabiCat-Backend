# 获取 Forest Cookie

> Chrome拓展与移动App都可获得Cookie。

## chrome 拓展

* 打开 [forestapp.cc](https://forestapp.cc/) 并下载Chrome拓展程序。
* 登陆你的账户。
* 点击 `选项`

![](https://p1.meituan.net/dpgroup/40e08e7bbe562ae37a1c1332f3df274c207045.png)


* 点击 `检查`

![](https://p0.meituan.net/dpgroup/952096dd7adb6bdfe3c4acf5289f221c797601.png)

1. 在弹出的 DevTool中选择 `网络(Network)`
2. 在拓展中点击 `与Forest App同步`
3. 在DevTool中搜索 : `remember_token`
4. 选择任意一个请求
5. 在请求的标头中即可获得 `FOREST_SECRET`

![-w1320](https://p0.meituan.net/dpgroup/9679c8cf6e928c76f2922ff7ba6545d41266615.png)

## IOS 或 Android APP

* 下载 Forest App 并登陆.
* 打开一个抓包App。
* 打开 Forest App 并点击 `云端同步`
* 在抓包工具中寻找 Cookie:**remember_token**


![media/16400590615034.jpg](https://p0.meituan.net/dpgroup/ae72f4e525e1afcd3cfce9bf6b5e47361429315.png)
