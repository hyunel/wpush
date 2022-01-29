<div align=center><img src="docs/phone.jpg" width="400" alt="phone2"/></div>

<h1 align="center">WPush</h1>
<h6 align="center">使用成本极低的腾讯云函数搭建属于自己的推送服务</h6>


### Feature
- :tada: 超长消息持久化储存  
- :tada: 简单易用的 API 接口  
- :tada: 支持所有类型消息推送  
- :tada: 可选的数据库支持  
- :tada: 免维护, 一次部署稳定使用

### Get Started
#### 发送消息
> 若不提供 content 参数将发送普通的文本消息

- 发送一个最简单的消息  

`https://你的云函数地址/send?secret=你配置的密钥&tittle=测试一下`

- 发送一个带有内容的卡片消息  

`https://你的云函数地址/send?secret=你配置的密钥tittle=测试一下&content=这是消息的内容blablablabla`

- 当然, 也可以通过 POST 请求发送
```json
POST /send

{
  "secret": "你配置的密钥",
  "tittle": "测试一下",
  "content": "这是消息的内容blablablabla"
}
```

- 你可以添加 `to` `tag` `party` 参数来筛选发送的企业成员
```json
POST /send

{
  "to": "USER_ID1|USER_ID2",
  "tag": "TAG_ID1|TAG_ID2",
  "party": "PARTY_ID",
  "secret": "你配置的密钥",
  "tittle": "测试一下",
  "content": "这是消息的内容blablablabla"
}
```

这些参数也可以是数组：
```json
POST /send

{
  "to": ["USER_ID1", "USER_ID2"],
  "tag": ["TAG_ID1", "TAG_ID2"],
  "party": ["PARTY_ID1", "PARTY_ID2"],
  "secret": "你配置的密钥",
  "tittle": "测试一下",
  "content": "这是消息的内容blablablabla"
}
```

- 发送一个高级的富文本消息
> 更多类型的消息可以查看[企业微信文档](https://work.weixin.qq.com/api/doc/90000/90135/90236#%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B)

```json
POST /send_rich

{
  "secret": "你配置的密钥",
  "type": "markdown",
  "data": {
    "content": "# 消息标题\n## 二级标题\n> 引用测试\n\n[baidu](https://baidu.com)"
  }
}
```


#### 展示消息
> 目前仅提供对卡片消息的展示, 

- 使用数据库: `https://你的云函数地址/show/消息ID`
- 未使用数据库: `https://你的云函数地址/show?t=TIME&h=TITTLE&c=CONTENT`


### 搭建 & 部署
详细搭建教程, [点我查看](docs/scf.md)

