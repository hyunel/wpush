<div align=center><img src="docs/phone.jpg" width="400" alt="phone2"/></div>

<h1 align="center">WPush</h1>
<h6 align="center">使用云函数搭建属于自己的推送服务</h6>


### Feature
- :tada: 超长消息持久化储存  
- :tada: 简单易用的 API 接口  
- :tada: 支持所有类型消息推送  
- :tada: 可选的数据库支持  
- :tada: 免维护, 一次部署稳定使用

### Get Started
#### 发送消息
- 参数说明

  |  参数   |                           说明                           |
  | :-----: | :------------------------------------------------------: |
  |  type   |                    消息类型，默认text                    |
  |  title  |             标题，在textcard、news类型中必填             |
  | content |             内容，在text、markdown类型中必填             |
  |   url   | 跳转链接，默认展示消息页面<br>仅markdown、news类型中生效 |
  |   pic   |         图片，默认Bing每日一图，仅news类型中显示         |

  | type参数 |      说明      |
  | :------: | :------------: |
  |   text   | 文本消息，默认 |
  | textcard |  文本卡片消息  |
  | markdown |  markdown消息  |
  |   news   |    图文消息    |
  
- 发送文本消息

  GET

  ```
  https://你的云函数地址/send?type=text&secret=你配置的密钥&content=这是消息的内容blablablabla
  ```
  
  POST /send

  ```json
  {
      "secret": "你配置的密钥",
      "type":"text",
      "content": "这是消息的内容blablablabla"
  }
  ```
  
  
  
- 发送文本卡片消息  

  GET

  ```
  https://你的云函数地址/send?secret=你配置的密钥&type=textcard&title=测试一下&content=这是消息的内容blablablabla
  ```

  POST /send

  ```json
  {
      "secret": "你配置的密钥",
      "type":"textcard",
      "title":"测试一下",
      "content": "这是消息的内容blablablabla"
  }
  ```

- 你可以添加 `to` `tag` `party` 参数来筛选发送的企业成员

  ```json
  {
      "to": "USER_ID1|USER_ID2",
      "tag": "TAG_ID1|TAG_ID2",
      "party": "PARTY_ID",
      "secret": "你配置的密钥",
      "type":"textcard",
      "title":"测试一下",
      "content": "这是消息的内容blablablabla"
  }
  ```

  这些参数也可以是数组：

  ```json
  {
      "to": ["USER_ID1", "USER_ID2"],
      "tag": ["TAG_ID1", "TAG_ID2"],
      "party": ["PARTY_ID1", "PARTY_ID2"],
      "secret": "你配置的密钥",
      "type":"textcard",
      "title":"测试一下",
      "content": "这是消息的内容blablablabla"
  }
  ```

  

- 发送Markdown消息

  GET

  ```
  https://你的云函数地址/send?secret=你配置的密钥&type=markdown&title=测试一下&content=这是消息的内容blablablabla
  ```

  POST /send
  
  ```json
  {
      "secret": "你配置的密钥",
      "type": "markdown",
      "content": "# 消息标题\n## 二级标题\n> 引用测试\n\n[baidu](https://baidu.com)"
  }
  ```
  
  

- 发送图文消息

  GET

  ```
  https://你的云函数地址/send?secret=你配置的密钥&type=news&title=测试一下&content=这是消息的内容blablablabla&pic=https://cn.bing.com/th?id=OHR.YosemiteNightSky_ZH-CN5864740024_1920x1080.jpg&url=https://www.baidu.com
  ```

  POST /send

  ```json
  {
      "secret": "你配置的密钥",
      "type": "news",
      "title": "测试一下",
      "content": "这是消息的内容blablablabla",
      "pic": "https://cn.bing.com/th?id=OHR.YosemiteNightSky_ZH-CN5864740024_1920x1080.jpg",
      "url":"https://www.baidu.com"
  }
  ```

  

#### 展示消息
> 目前仅提供对卡片消息、图文消息进行展示 

- 使用数据库: `https://你的云函数地址/show/消息ID`
- 未使用数据库: `https://你的云函数地址/show?t=TIME&h=TITLE&c=CONTENT`


### 搭建 & 部署
> **2022-04-23 更新**:  
> 因为腾讯云函数 5 月 23 日后不再提供免费额度，不建议再使用 [腾讯云函数搭建](docs/scf.md)  
> 推荐使用 **Vercel** 作为替代，目前已添加对 **Vercel** 的支持

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fhyunel%2Fwpush&env=SYS_URL,API_SECRET,CORP_ID,CORP_SECRET,AGENT_ID&envDescription=Configuration%20needed%20for%20WPush&envLink=https%3A%2F%2Fgithub.com%2Fhyunel%2Fwpush%2Fblob%2Fmaster%2Fconfig.py&project-name=wpush&repo-name=wpush)