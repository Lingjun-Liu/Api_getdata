# 🔌 理解 API：通过API获取数据指南

## 📋 目录

- [一、什么是 API？](#一什么是-api)
- [二、API 的核心功能：超越数据读取](#二api-的核心功能超越数据读取)
- [三、API 的来源、治理与访问模型](#三api-的来源治理与访问模型)
- [四、API 与爬虫的区别](#四api-与爬虫的区别)
- [五、API 的使用流程（从申请到抓取）](#五api-的使用流程从申请到抓取)
- [六、现有的学术研究中的实践](#六个人使用过的api)
- [七、国内API使用情况](#七国内api使用情况)

---

基于大数据做研究已经成为社会科学领域研究的新趋势，但是实际上**如何获取大数据**并没有人很好的介绍过这个部分内容。一部分权威机构/学者是可以购买或者通过一些课题项目获取一些大数据资源的，但是我们硕博生就比较惨很难自己弄到这样的数据。
但是在科研项目中，数据的获取方式往往直接决定了研究的可行性与质量。常见的两种数据抓取方式是 **API（Application Programming Interface）** 和 **网页爬虫（Web Scraping）**。关于[网页爬虫](https://github.com/Lingjun-Liu/Web_scraping)获取数据在这个repository里有介绍，但是坦白的讲这种方式可以用来爬取一些自己懒得复制粘贴的数据最好；如果是用做文本分析呀这数据的合规性就很难说得清了，而且获取的数据结构性也比较差，不适合深入研究。最好还是通过API获取。

- 在**数据驱动的科研时代**，API 是通往结构化数据与平台能力的第一道门槛；
- 真正理解 API 的架构、认证、配额与限流机制，能帮助你**建立稳定、复现、合规**的数据抓取管道；
- API 的治理设计思想，也逐步成为理解平台运行逻辑（如社交推荐机制、信息分发规则）的工具。
这个部分将系统介绍**API的背景知识以及如何Via API获取数据**，帮助科研工作者选择合适的技术路径。
> 📎 **本文由作者参考以下相关资料整理 **
 > - [An illustrated introduction to APIs](https://medium.com/epfl-extension-school/an-illustrated-introduction-to-apis-10f8000313b9)
 > - [Intro to APIs](https://medium.com/@rwilliams_bv/apis-d389aa68104f)
 > - [Lab Video Lecture: Intro to APIS for Computational Social Scientists](https://youtu.be/OD40nwKuVB8)
 > - [使用API](https://melaniewalsh.github.io/Intro-Cultural-Analytics/04-Data-Collection/05-What-Is-API.html)
 > - [Blog about socail network API](https://rtweet.info/)


当然在这部分开始之前必须强调在学术研究中使用这种方法的规范准则和注意事项，这个部分参考[User's data:legal & ethical considerations](https://melaniewalsh.github.io/Intro-Cultural-Analytics/04-Data-Collection/01-User-Ethics-Legal-Concerns.html)
---

## 一、什么是 API？

### 1.1 核心定义：API 到底是什么？

**API**（Application Programming Interface，应用程序编程接口）本质上是一个**软件中介**，它是一组预先定义好的规则、协议和工具，用于构建和集成应用程序。
- 如果说 **UI（用户界面）** 是人类与软件交互的界面，那么 **API** 就是**软件与软件交互的界面**。

> **API（应用程序编程接口）是现代数字科研与开发的“基础设施”**，它们让不同平台之间的数据与功能得以结构化地互通，同时隐藏了底层的技术复杂性。  
> 从人文学者收集文化数据，到社会科学家分析 Twitter 社交网络，API 已成为不可或缺的工具。  
> 然而，它们也是一种“被政治化的技术”——平台通过 API 控制着研究者能访问什么数据、以何种方式访问。

### 1.2 API 的核心价值：抽象与封装

- **抽象（Abstraction）**  
  提供一个清晰、简化的功能列表（如"获取天气"、"创建订单"），隐藏实现这些功能的复杂逻辑。

- **封装（Encapsulation）**  
  定义严格的"合同"（Contract），调用者只能通过合同访问特定数据和功能，保护系统内部的稳定性和安全性。

> **简而言之：** API 允许一个软件（客户端）向另一个软件（服务器）发送结构化请求，并接收结构化响应，而无需了解对方的内部实现。

### 1.3 API的技术架构：HTTP、REST 与 CRUD

### 1. HTTP 协议：通信的基础

> HTTP（超文本传输协议）是客户端与服务器之间通信的标准。  
> 虽然有 8 种 HTTP 方法，但日常只用 4 种：GET、POST、PUT、DELETE。  

> 请求-响应循环是基本模式：  
> 客户端发请求 → 服务器处理并返回 → 客户端解析。  

> 状态码语义：  
> - 2xx：成功  
> - 3xx：重定向  
> - 4xx：客户端错误  
> - 5xx：服务器错误  

### 2. CRUD 操作：数据的四种基本动作

| 动作 | HTTP 动词 | 示例 |
|------|------------|------|
| 创建 | POST       | 发一条推文 |
| 读取 | GET        | 获取用户信息 |
| 更新 | PUT        | 修改资料 |
| 删除 | DELETE     | 删除推文 |

### 3. REST 架构：设计规范

> REST（Representational State Transfer）是 Roy Fielding 提出的架构风格，现为 HTTP API 的主流标准。  
> 它有六大约束：

1. **统一接口**：URL 结构清晰，动词标准化，响应码统一。  
2. **无状态**：每个请求都包含全部信息，服务器不“记”你是谁。  
3. **可缓存**：响应明确是否可缓存，提升性能。  
4. **客户端-服务器分离**：双方可独立演化。  
5. **分层系统**：负载均衡、缓存、安全层对客户端透明。  
6. **按需代码（可选）**：服务器可把代码片段下发给客户端执行。


## 二、API 的核心功能：超越数据读取

API 并不仅限于数据读取（Read），它覆盖了数据及业务逻辑的完整生命周期 —— 即 **CRUD（Create, Read, Update, Delete）操作**。

### 2.1 HTTP 方法与操作对照

| 操作   | 方法   | 描述 | 示例 |
|--------|--------|------|------|
| **创建** | POST   | 创建新资源。请求体中包含数据。 | `POST /api/v1/users` 创建新用户 |
| **读取** | GET    | 检索一个或多个资源。 | `GET /api/v1/users/123` 获取用户信息 |
| **更新** | PUT / PATCH | 修改现有资源。<br>PUT 替换全部；PATCH 修改部分字段。 | `PATCH /api/v1/users/123` 仅更新邮箱 |
| **删除** | DELETE | 删除指定资源。 | `DELETE /api/v1/users/123` 删除用户 |



---

## 三、API 的来源、治理与访问模型

API 的管理方式决定了它的可见性与用途，主要有以下几种类型：

### 3.1 API 分类

| 类型 | 定义 | 用途 |
|------|------|------|
| **内部 API（Private APIs）** | 仅组织内部使用，不公开。 | 构建微服务架构，前后端通信。 |
| **外部 API（Public/Open APIs）** | 向所有开发者开放。 | 第三方应用集成平台功能，例如地图、支付等。 |
| **合作伙伴 API（Partner APIs）** | 仅授权合作伙伴可用。 | 用于 B2B 集成，如银行与金融科技公司对接。 |

### 3.2 访问控制机制

API 的访问通常受到严格的认证与授权机制保护，主要有两种方式：

#### 3.2.1 API Key（API 密钥）

- **是什么：** 一个唯一的 token，用于识别调用方（应用）。
- **放置位置：** 通常在 HTTP 请求头部（如：`x-api-key: YOUR_KEY`）。
- **作用：**
  - 识别调用方身份
  - 用于调用次数统计和速率限制
  - 阻止匿名非法访问

#### 3.2.2 OAuth 2.0（更高级的授权）

- **是什么：** 一个行业标准的**授权框架**
- **区别：**
  - API Key 验证的是"应用"
  - OAuth 授权的是"用户"的数据访问权限
- **应用场景：** 使用微信/谷歌登录就是 OAuth 的应用 —— 用户授权应用访问其在第三方平台上的信息，而无需泄露密码。

> **总结：** OAuth 实现了安全的委托授权（Delegated Authorization），是现代互联网服务的重要安全基础。

---

## 四、API 与爬虫的区别

| 比较维度 | API | 爬虫（Web Scraping） |
|----------|-----|---------------------|
| 数据源 | 平台主动提供的结构化接口 | 网页呈现给用户的 HTML 内容 |
| 结构稳定性 | 高：字段明确、版本控制 | 低：页面结构易变，需频繁维护 |
| 法律合规性 | 高：在授权与条款下使用 | 有风险：需遵守网站 ToS、robots.txt |
| 技术门槛 | 中等：需理解文档、申请密钥 | 低-中：启动快但后期维护成本高 |
| 访问速率 | 明确限流（如每分钟/天次数） | 可并发扩展，但易被封禁 |
| 典型用途 | 公众数据分析、平台研究、实时服务 | 页面内容补抓、字段缺失补全、结构化抽取 |

🧭 **研究者优先考虑 API**：它更利于项目的复现性、数据质量控制与合规性管理。

---


### 📚 更为专业的一些API的内容

以下资料有助于深入理解 API 的架构理念、认证机制及设计规范，适合系统性学习者或准备开发/设计 API 的同学：

- [OpenAPI Specification](https://swagger.io/specification/)  
  详解如何使用 OpenAPI（原 Swagger）标准来定义和文档化 RESTful API。

- [OAuth 2.0 简介与流程](https://oauth.net/2/)  
  官方权威资源，涵盖 OAuth 2.0 各种授权流程及使用场景。

- [Google Cloud API Design Guide](https://cloud.google.com/apis/design)  
  Google 官方的 API 设计最佳实践，强调一致性、可扩展性与安全性。

- [RESTful API Design Guidelines](https://github.com/microsoft/api-guidelines)  
  微软开源的 REST API 设计指南，涵盖命名规范、版本控制、错误处理等细节。

---

### 🧪 API 实践资源（适合练手）

以下是一些无需复杂配置或授权，即可直接用于练手、测试和开发原型的 API：

| 名称 | 类型 | 特点 |
|------|------|------|
| [JSONPlaceholder](https://jsonplaceholder.typicode.com/) | 模拟数据 | 免费、无需认证，API练习场，适合练习 CRUD 操作 |
| [Reddit API](https://www.reddit.com/dev/api/) | 社交内容 | 适合话题挖掘、情绪分析，支持多种查询，或许也可以使用[PRAW](https://praw.readthedocs.io/en/latest/getting_started/installation.html) |
| [Twitter/X API](https://developer.twitter.com/en/docs/twitter-api) | 社交媒体 | 强大但需授权，适合话语权、社群研究 |
| [GitHub API](https://docs.github.com/en/rest) | 开发者社区 | 获取代码、贡献者、项目关系网络等数据 |
| [Spotify API](https://developer.spotify.com/documentation/web-api) | 媒体推荐 | 支持获取歌曲、歌单、推荐系统数据，需授权 |

> 💡 **建议搭配**：Postman 或 Hoppscotch，用于模拟请求、理解 Header、查询参数等结构。

---

### 🌐 API 聚合与探索平台

这些平台汇集了多个 API 接口，并提供统一的管理和调用方式，适合快速寻找可用数据源、批量测试和对比接口能力：

| 平台名称 | 链接 | 简介 |
|-----------|------|------|
| [RapidAPI](https://rapidapi.com/) | 全球最大 API 市场之一 | 提供统一接口、调用分析、速率控制、付费订阅等功能 |
| [Postman API Network](https://www.postman.com/explore) | API 共享与测试平台 | 包含大量官方或第三方 API，可直接导入测试 |
| [Hoppscotch](https://hoppscotch.io/) | 开源 API 调试平台 | 可创建 API 调用模板，支持实时测试与分享 |
| [API List](https://apilist.fun/) | 精选公共 API 列表 | 重点收录有趣、有用的免费接口，适合创意开发 |
| [ProgrammableWeb](https://www.programmableweb.com/) | 历史悠久的 API 数据库 | 提供 API、Mashup、SDK 信息，但更新频率下降 |
| [Public APIs GitHub](https://github.com/public-apis/public-apis) | 开源 API 汇总 | 社区驱动维护的免费 API 清单，涵盖多个类别 |

---

> 💡 **个人的一点体会Tips for 学术科研者**：
>
> - 使用之前需要了解这个平台，至少要知道他的有哪些信息、是如何发布的、传播的流程和机制以及覆盖面等等
> - 另外很多的大平台已经发展出了一些封装好的R包以及py包，可以直接使用
> - 注意每个 API 的使用政策、速率限制与数据授权许可，确保研究合规性。

## 六、现有的学术研究中的实践
目前的社会科学研究领域用到的大数据包括但不限于：经济数据、天气数据、地理数据、社交文本数据
简单的做一个总结小表格：
### 📊 大数据类型与典型社会科学应用一览表

| 大类 | 数据类型 | 具体数据内容 | 数据来源/收集方式 | 典型社会科学应用领域 |
|------|-----------|----------------|---------------------|----------------------|
| **I. 互联网与社交媒体数据** | 社交文本数据 | 用户发帖、评论、博客、新闻评论、论坛讨论等 | 社交平台（微博、微信、Twitter/X、Facebook）、新闻网站、论坛 | 舆情分析、民意调查、情感分析、文化变迁、公共卫生（疫情追踪） |
|  | 网络行为数据 | 搜索记录、点击流、网站访问时长、用户浏览路径等 | 搜索引擎、电商平台、各类 App、网站日志 | 消费者行为研究、信息获取模式、知识传播、媒体素养 |
|  | 网络结构数据 | 好友关系、关注关系、群组连接、信息分享路径 | 社交媒体平台、电子邮件通信记录 | 社会网络分析、信息扩散模型、群体动力学、组织行为学 |
|  | 多媒体数据 | 图片、视频、直播、音频记录 | 社交媒体、视频平台（YouTube、抖音）、在线图库 | 视觉社会学、文化人类学、内容分析、事件识别 |
| **II. 行为轨迹与移动数据** | 移动通信数据 | 手机信令、通话记录（CDR）、粗略定位数据 | 移动运营商、通信基站 | 人口流动、城市通勤、区域经济活动、灾害应急管理 |
|  | 地理位置数据（LBS） | GPS 记录、App 定位数据、签到记录 | 智能手机应用、LBS 服务商 | 犯罪地理学、城市空间结构、休闲活动分析、旅游研究 |
|  | 交通运输数据 | 公交/地铁刷卡、出租车轨迹、航空/铁路票务记录 | 交通管理部门、网约车平台、公共交通系统 | 职住分离、交通规划、可达性研究、城市社会学 |
| **III. 商业与交易数据** | 金融与消费数据 | 银行交易、第三方支付、电商交易、POS 数据 | 银行、支付平台、电商平台、零售商 | 宏观经济监测、收入差异、消费者行为、金融行为学 |
|  | 企业运营数据 | 供应链数据、CRM、HR 数据等 | 企业内部信息系统 | 管理学、劳动经济学、组织行为、产业结构研究 |
| **IV. 行政管理与公共服务数据** | 政府行政记录 | 出生/死亡登记、税务、教育、医疗、法院文书 | 各级政府、公共机构（需脱敏） | 公共政策评估、人口研究、医疗卫生经济学、司法研究 |
|  | 城市运行数据 | 空气质量、噪音、水电气用量、垃圾处理、交通流量 | 智慧城市平台、环境监测站、公用事业公司 | 城市治理、环境社会学、能源研究、可持续发展 |
|  | 气象与环境数据 | 历史天气、实时气象、污染指数、气候监测 | 气象局、环保部门、遥感平台 | 灾害社会学、农业经济学、气候变化与社会研究 |
---
> 小总结 API 如何改变研究范式
> - 1. 核心方法
网络分析（谁转发谁）、情感分析（推文情绪）、地理分析（推文位置）、时间序列（事件演化）
> - 2. 数据来源
政治传播、舆情; 社群文化; 音乐消费; 媒体框架; 人口统计(Census API)



## 五、API 的使用流程（从申请到抓取）

使用 API 获取数据，通常遵循以下步骤：

### 5.1 基本的Step-by-step 流程

1. **阅读文档**：理解端点、参数、返回字段与限流策略；
2. **注册开发者账号**：申请 API Key 或 OAuth 凭证；
3. **构造请求**：使用如 `requests`、`httpx` 等库，构建 URL、Headers、Body；
4. **处理认证**：
   - 简单认证：在请求头中加入 API Key；
   - OAuth 认证：通过用户授权，获取访问 Token；
5. **分页控制**：处理数据过多时的分页机制（如 page/limit 或 next_token）；
6. **速率控制与容错处理**：
   - 响应码 `429 Too Many Requests` 表示被限流；
   - 应使用**指数退避**策略（Exponential Backoff）自动重试；
7. **结果存储与管理**：将 JSON 数据结构化保存为 CSV、数据库或 Parquet 格式；
8. **确保可复现性**：保存请求配置、数据字典、日志文件等。
### 5.2 几点使用和注意的小Tips：认证与安全：API 钥匙不是“万能钥匙”
1. 认证流程（以 Twitter 为例）
> 1. 注册普通账号  
> 2. 申请开发者权限（填表，通常 24 小时内批）  
> 3. 创建“应用”，填名称、描述、网址  
> 4. 平台生成四把钥匙：  
>    - API Key  
>    - API Secret Key  
>    - Access Token  
>    - Access Token Secret  

2. 安全最佳实践
> **不要把钥匙写死在代码里！**  
> 推荐做法：  
> ```python
> # api_key.py
> your_token = "YOUR_REAL_TOKEN"
>
> # main.py
> import api_key
> token = api_key.your_token
> ```
> R 的 rtweet 包更优雅：  
> ```r
> create_token(
>   app = "my_app",
>   consumer_key = "YOUR_KEY",
>   consumer_secret = "YOUR_SECRET"
> )
> ```
> 钥匙自动存为环境变量，下次开机直接用。
3. 政治现实：平台说了算
> - Twitter 免费接口只能看 **14 天内推文**  
> - 剑桥分析事件后（[Cambridge Analytica scandal](https://en.wikipedia.org/wiki/Facebook%E2%80%93Cambridge_Analytica_data_scandal)），Facebook **大幅收紧权限**  

> **API 是“民主”的，但平台决定你“民主”到什么程度。**


## 七、国内API使用情况
国内有使用API通道开放的数据并不多，有一些数据可以通过一些课题申请获得，但是大多数数据都是不开放给普通研究者的，所以大家只能自己爬取或者依托一些课题项目进行使用。
很多社交平台自己把这些数据做成了生意，比如新浪微博自己做了[新浪舆情通](https://yqt.midu.com/?webGamesType=1&industryType=1&unit=%E8%88%86%E6%83%85PC&keyword=%E5%BE%AE%E5%8D%9AAPI&bd_vid=10645369010028577718)；小红书的开发者平台我去看了也是不开放给研究人员的，主要是用于营销分析的[小红书 Marketing API](https://ad-market.xiaohongshu.com/docs-center?bizType=943&articleId=4437)；[淘宝](https://open.taobao.com/doc.htm?docId=73&docType=1)有开放平台，也是主要针对企业的；还有[豆瓣api](www.doubanapi.com)但是也不知道是不是官方的……

简单找到了几个可以使用的API，用了一下，见下：

### 1.气象数据的API调用
国内的[国家气象科学数据中心](https://data.cma.cn/ai/#/search)，允许使用api接口下载数据。虽然我也用不上这个数据，但是找到了一份非常详细的资料，需要自取[调用CMDC API下载中国气象网公开数据](https://mp.weixin.qq.com/s/DofkH6pDAsVLvfpoHFgYwg)

### 2.地图数据之POI数据
之前的组会的时候听做城市圈研究的张琳师妹分享过POI（Point Of Interests）数据的相关介绍，感觉挺好玩的，经济学也有很多用POI数据构造一些工具变量。
国内百度、高德和腾讯都开放了API获取数据，但是年份有些不全，所以使用的时候还是自己甄别：
这边附上一个链接是关于三个平台API对比的：[三大地图开放平台对比——Web API篇](https://mp.weixin.qq.com/s/Kod76uOAT0vBeoP491QjLA)
举个例子
- [高德获取POI数据](https://github.com/Lingjun-Liu/Api_getdata/GaoDe_POI_via_APIs)的例子

### 3.使用API集合 
大部分都是收费的，充值之后可以使用，而且是低代码基本基于UI操作即可。






