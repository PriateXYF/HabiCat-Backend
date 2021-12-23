# HabiCat-Backend

> HabiCat 后端实现

## 部署方式

> **无需服务器、域名**，基于 LeanCloud 一键部署。

1. 在 [LeanCloud国际版](https://leancloud.app) 上注册一个账号，并登陆控制台。
2. 创建一个应用，应用名可任意设置，如 : HabiCat 。
3. 进入 `云引擎` ->  `设置` ，设置好必要的环境变量。
    * **HABITICA_USERID** `必填` : 你的 Habitica 用户ID
    * **HABITICA_SECRET** `必填` : 你的 Habitica API令牌
    * **PUSH_PLUS** `选填` : [Push Plus](http://www.pushplus.plus/) 的 token (用于通知).
4. 在 `共享域名` 处设置你的域名，将来可以直接用此域名访问，如果有自己的域名也可以设置 `自定义域名` 。
5. 进入 `云引擎` ->  `部署` ，选择部署方式为 `Git部署` ，地址为本项目地址 `https://github.com/PriateXYF/HabiCat-Backend.git` 。
    * 其余参数默认即可
    * 若部署失败请重复尝试，或选择 `不使用缓存` 。
6. 部署成功后使用你的域名即可正常访问。

## 集成

* 不背单词 [说明](docs/bbdc.md)
* Forest [说明](docs/forest.md)