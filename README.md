# HabiCat-Backend

> HabiCat 后端实现

## 部署方式

> **无需服务器、域名**，基于 LeanCloud 一键部署。

1. 在 [LeanCloud国际版](https://leancloud.app) 上注册一个账号，并登陆控制台。
2. 创建一个应用，应用名可任意设置，如 : HabiCat 。
3. 进入 `云引擎` ->  `设置` ，设置好必要的环境变量。
    * **HABITICA_USERID** `必填` : 你的 Habitica 用户ID
    * **HABITICA_SECRET** `必填` : 你的 Habitica API令牌
    * **PUSH_PLUS** `选填` : [Push Plus](http://www.pushplus.plus/) 的 token (用于接收通知)
4. 在 `共享域名` 处设置你的域名，将来可以直接用此域名访问，如果有自己的域名也可以设置 `自定义域名` 。
5. 进入 `云引擎` ->  `部署` ，选择部署方式为 `Git部署` 。
    * 地址为本项目地址 https://github.com/PriateXYF/HabiCat-Backend.git 。
    * 将分支或提交设置为 `main`
    * 若部署失败请**重复尝试**，或选择 `不使用缓存` 。
6. 部署成功后使用你的域名即可正常访问。
7. 在运行过程中如果出现任何问题可以自行前往 `云引擎` -> `WEB` -> `日志` 中定位。

## 其他配置

应用的配置都在 `数据存储` -> `结构化数据` -> `Projects` 中。其可修改的字段含义分别为:

* habitName : Habitica习惯的名字。
* isShow : 是否显示该模块。
* isOpen : 该模块是否加密。
* password : 模块解锁的密码。

## 集成

* 不背单词 [说明](docs/bbdc.md)
* Forest [说明](docs/forest.md)

## 其他

* 如果有需要支持的网站或APP可以在 issue 中提出。
* 如果部署出现问题自行前往 `云引擎` -> `WEB` -> `日志` 中定位。
* 赞助方式 [![](https://donate.virts.app/images/pay/all.jpg)](https://donate.virts.app)

## 预览

![](https://p0.meituan.net/dpgroup/53b8c5f7876cc73d2c6882b8bc85405a185033.png)
![](https://p0.meituan.net/dpgroup/d425fe6b248a70a988a4d6340cfe227d273651.png)
![](https://p1.meituan.net/dpgroup/bf49e29871562693cfc0dbbfc64e7c39259524.png)