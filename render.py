import config

sys_url = config.get('sys_url')
index_html = '''
<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://unpkg.com/vue@3.2.33/dist/vue.global.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/element-plus@2.2.2/dist/index.css">
    <script src="https://unpkg.com/element-plus@2.2.2/dist/index.full.js"></script>
    <script src="https://unpkg.com/@element-plus/icons-vue@1.1.4/dist/index.iife.min.js"></script>
    <link rel="icon" href="https://fastly.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.1.1/svgs/regular/comments.svg">
    <title>WPUSH</title>
</head>

<body>

    <div id="app" v-cloak>
        <!-- 发送消息 -->
        <section>
            <a href="https://github.com/hyunel/wpush" class="github-corner" aria-label="View source on GitHub">
                <svg width="80" height="80" viewBox="0 0 250 250"
                    style="fill:#70B7FD; color:#fff; position: absolute; top: 0; border: 0; right: 0;"
                    aria-hidden="true">
                    <path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path>
                    <path
                        d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2"
                        fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path>
                    <path
                        d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z"
                        fill="currentColor" class="octo-body"></path>
                </svg>
            </a>
            <div class="container">
                <div class="form">
                    <div class="title">
                        <div class="image">
                            <img
                                src="https://fastly.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.1.1/svgs/regular/comments.svg" />
                        </div>
                        <span>WPUSH</span>
                    </div>
                    <div>
                        <el-form ref="elForm" :model="formData" :rules="rules" size="default" label-width="auto"
                            label-position="right" :key="key">
                            <el-form-item label="全 员" prop="all" size="large" style="margin-bottom: 18px;">
                                <el-switch v-model="all" border-color="white" size="large" />
                            </el-form-item>
                            <el-form-item label="人 员" v-show="!all" prop="user">
                                <el-input v-model="user" placeholder="人员ID，以空格分隔" clearable :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="标 签" v-show="!all" prop="tag">
                                <el-input v-model="tag" placeholder="标签ID，以空格分隔" clearable :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="部 门" v-show="!all" prop="party">
                                <el-input v-model="party" placeholder="部门ID，以空格分隔" clearable :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="类 型" prop="type">
                                <el-select v-model="formData.type" :disabled="disabled" @change="selectType">
                                    <el-option v-for="(item, index) in typeOptions" :key="index" :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="秘 钥" prop="secret">
                                <el-input v-model="formData.secret" placeholder="访问秘钥" clearable show-password
                                    :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="图 片" prop="pic" v-show="formData.type =='news'">
                                <el-input v-model="formData.pic" placeholder="含协议头(http/https)" clearable
                                    :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="跳 转" prop="url"
                                v-show="formData.type =='textcard'||formData.type=='news'">
                                <el-input v-model="formData.url" placeholder="含协议头(http/https)" clearable
                                    :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="标 题" prop="title"
                                v-show="formData.type =='textcard'||formData.type=='news'">
                                <el-input v-model="formData.title" placeholder="消息标题" clearable :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="摘 要" prop="summary"
                                v-show="formData.type =='textcard'||formData.type=='news'">
                                <el-input v-model="formData.summary" placeholder="消息摘要" clearable :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="内 容" prop="content">
                                <el-input v-model="formData.content" type="textarea" placeholder="消息内容"
                                    :autosize="{minRows: 4, maxRows: 4}" :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item size="large" class="btn" label-width="0">
                                <el-button type="primary" @click="submitForm" round size="large" :disabled="disabled">
                                    <el-icon style="vertical-align: middle;" :size="20" v-show="!disabled">
                                        <Finished />
                                    </el-icon>
                                    <el-icon style="vertical-align: middle;" :size="20" v-show="disabled">
                                        <Loading />
                                    </el-icon>
                                    <span style="vertical-align: middle;font-weight: bold;">
                                        {{disabled?'发 送 中':'发 送'}}</span>
                                </el-button>
                                <el-button @click="resetForm" round size="large" :disabled="disabled">
                                    <el-icon style="vertical-align: middle;" :size="20">
                                        <Refresh />
                                    </el-icon>
                                    <span style="vertical-align: middle;font-weight: bold;">重 置</span>
                                </el-button>
                            </el-form-item>
                        </el-form>
                    </div>
                </div>
            </div>
        </section>
    </div>
</body>
<style>
    .github-corner:hover .octo-arm {
        animation: octocat-wave 560ms ease-in-out;
    }

    @keyframes octocat-wave {

        0%,
        100% {
            transform: rotate(0)
        }

        20%,
        60% {
            transform: rotate(-25deg)
        }

        40%,
        80% {
            transform: rotate(10deg)
        }
    }

    @media (max-width:500px) {
        .github-corner:hover .octo-arm {
            animation: none
        }

        .github-corner .octo-arm {
            animation: octocat-wave 560ms ease-in-out
        }
    }

    [v-cloak] {
        display: none;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        background: linear-gradient(to bottom right, #0184cf, #77A1D3, #a0eacf);
    }

    section {
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
    }

    section .color {
        position: absolute;
        filter: blur(200px);
    }

    .title {
        margin-bottom: 20px;
    }

    .image {
        display: inline-block;
        overflow: hidden;
        vertical-align: middle;
    }

    .image img {
        position: relative;
        left: -100px;
        filter: drop-shadow(#ffffff 100px 0);
        width: 40px;
    }

    .title span {
        color: #fff;
        font-size: 24px;
        font-weight: 600;
        letter-spacing: 5px;
        margin-left: 10px;
        vertical-align: middle;
    }


    .container {
        position: relative;
        width: 360px;
        min-height: 400px;
        background: rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(5px);
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }

    .form {
        position: relative;
        width: 100%;
        height: 100%;
        padding: 50px;
    }

    .el-form-item__label {
        color: white;
        font-weight: bold;
        font-size: 15px !important;
    }

    .el-message-box {
        width: 300px;
    }

    .btn {
        margin-bottom: 0px !important;
    }

    .btn .el-form-item__content {
        margin-left: 0px !important;
        display: flex;
        justify-content: space-between
    }

    .el-textarea__inner {
        padding: 5px 11px !important;
    }
</style>
<script src="https://unpkg.com/axios@0.27.2/dist/axios.min.js"></script>
<script>
    const App = {
        data() {
            return {
                key: 0,
                disabled: false,
                link: "",
                all: true,
                user: "",
                tag: "",
                party: "",
                formData: {
                    user: "",
                    tag: "",
                    party: "",
                    secret: "",
                    title: "",
                    summary: "",
                    content: "",
                    pic: "",
                    url: "",
                    type: "text",
                },
                rules: {
                    secret: [{
                        required: true,
                        message: '请输入秘钥',
                        trigger: 'blur'
                    }],
                    type: [{
                        required: true,
                        message: '请选择消息类型',
                        trigger: 'change'
                    }],
                    pic: [{
                        required: false,
                        message: '请输入图片链接',
                        trigger: 'blur'
                    }],
                    url: [{
                        required: false,
                        message: '请输入跳转链接',
                        trigger: 'blur'
                    }],
                    title: [{
                        required: false,
                        message: '请输入消息标题',
                        trigger: 'blur'
                    }],
                    summary: [{
                        required: false,
                        message: '请输入消息摘要',
                        trigger: 'blur'
                    }],
                    content: [{
                        required: true,
                        message: '请输入消息内容',
                        trigger: 'blur'
                    }],
                },
                typeOptions: [{
                    "label": "文本消息",
                    "value": "text"
                }, {
                    "label": "文本卡片",
                    "value": "textcard"
                }, {
                    "label": "Markdown",
                    "value": "markdown"
                }, {
                    "label": "图文消息",
                    "value": "news"
                }],
            }
        },
        methods: {
            selectType(item) {
                this.key++
                if (item == "news" || item == "textcard") {
                    this.rules.title[0].required = true
                } else {
                    this.rules.title[0].required = false
                }
            },
            handleTarget() {
                if (this.all) {
                    this.formData.user = "@all"
                    this.formData.tag = ""
                    this.formData.party = ""
                } else {
                    if (this.user.trim() || this.tag.trim() || this.party.trim()) {
                        if (this.user.trim()) {
                            this.formData.user = this.user.trim().split(/\s+/)
                        } else {
                            this.formData.user = ""
                        }
                        if (this.tag.trim()) {
                            this.formData.tag = this.tag.trim().split(/\s+/)
                        } else {
                            this.formData.tag = ""
                        }
                        if (this.party.trim()) {
                            this.formData.party = this.party.trim().split(/\s+/)
                        } else {
                            this.formData.party = ""
                        }
                    } else {
                        this.formData.user = "@all"
                        this.formData.tag = ""
                        this.formData.party = ""
                    }
                }

            },
            submitForm() {
                this.disabled = true
                this.handleTarget()
                let content = this.formData.content
                this.formData.content = decodeURIComponent(content)
                this.$refs['elForm'].validate(valid => {
                    if (!valid) {
                        this.disabled = false
                        this.showErrorConfirm("请完整填写参数！")
                    }
                    else {
                        axios({
                            method: "post",
                            url: "<%SYSURL%/>/send",
                            data: JSON.stringify(this.formData).replace(/\\\\\\\\/g, "\\\\"),
                            headers: {
                                'Content-Type': 'application/json;charset=UTF-8'
                            }
                        }).then(resp => {
                            this.disabled = false
                            if (resp.data.code == '0') {
                                if (this.formData.type == 'text' || this.formData.type == 'markdown') {
                                    this.showSuccessConfirm("消息发送成功！")
                                } else {
                                    this.link = resp.data.link
                                    this.showLinkConfirm("消息发送成功，前往消息显示页？")
                                }
                            } else {
                                this.showErrorConfirm("消息发送失败，错误信息：" + resp.data.msg)
                            }
                        }).catch(err => {
                            this.disabled = false
                            this.showErrorConfirm("消息发送失败，请稍后再试~")
                        })
                    }
                })
            },
            resetForm() {
                this.all = true
                this.user = ""
                this.tag = ""
                this.party = ""
                this.formData = {
                    user: "",
                    tag: "",
                    party: "",
                    secret: "",
                    title: "",
                    summary: "",
                    content: "",
                    pic: "",
                    url: "",
                    type: "text",
                }
            },
            showLinkConfirm(msg) {
                this.$confirm(msg, '提示', {
                    confirmButtonText: '前往',
                    cancelButtonText: '返回',
                    type: 'success'
                }).then(() => {
                    this.resetForm()
                    window.open(this.link, "_self")
                }).catch((err) => { })
            },
            showSuccessConfirm(msg) {
                this.$confirm(msg, '提示', {
                    cancelButtonText: '返回',
                    showConfirmButton: false,
                    type: 'success'
                }).then().catch((err) => { })
            },
            showErrorConfirm(msg) {
                this.$confirm(msg, '提示', {
                    cancelButtonText: '返回',
                    showConfirmButton: false,
                    type: 'error'
                }).then().catch((err) => { })
            }
        }
    }
    const app = Vue.createApp(App);
    for ([name, comp] of Object.entries(ElementPlusIconsVue)) {
        app.component(name, comp);
    }
    app.use(ElementPlus);
    app.mount("#app");
</script>

</html>
'''
info_html = '''
<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="https://fastly.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.1.1/svgs/regular/comments.svg">
    <link rel="stylesheet" href="https://fastly.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">
    <title>WPUSH</title>
</head>

<body>
    <div id="app">
        <!-- 显示消息 -->
        <section>
            <div class="container">
                <h2 class="title">
                    <%TITLE%/>
                </h2>
                <div class="metabar">
                    <div class="time">
                        <i class="fa fa-clock-o"></i>
                        <span class="inner">
                            <%TIME%/>
                        </span>
                    </div>
                    <div class="count"><i class="fa fa-pencil"></i><span class="inner">0</span>字</div>
                </div>
                <article>
                    <pre><%CONTENT%/></pre>
                </article>
            </div>
        </section>
    </div>
</body>
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        background: linear-gradient(to bottom right, #0184cf, #77A1D3, #a0eacf);
    }

    .container {
        width: 90%;
    }

    .metabar>* {
        color: #fff;
        display: inline-block;
        font-size: 12px;
        margin-right: 7px;
        margin-bottom: 10px;
    }

    .metabar .fa {
        font-size: 14px;
        margin-right: 3px;
    }

    article {
        padding: 16px;
        background-color: white;
        border-radius: 8px;
        margin-bottom: 16px;
    }

    pre {
        white-space: pre-wrap;
        word-break: break-all;
        margin: 0px;
        font-size: 14px;
    }

    .title {
        font-size: 22px;
        margin: 15px 0 6px;
        color: #fff;
    }

    @media screen and (min-width: 768px) {
        .title {
            font-size: 28px;
        }
    }

    section {
        position: relative;
        overflow: hidden;
        display: flex;
        justify-content: center;
        min-height: 100vh;
    }
</style>
<script src="https://fastly.jsdelivr.net/npm/js-base64@3.6.1/base64.min.js"></script>
<script src="https://fastly.jsdelivr.net/npm/moment@2.29.1/moment.min.js"></script>
<script src="https://fastly.jsdelivr.net/npm/markdown@0.5.0/lib/markdown.min.js"></script>
<script>
    const params = new URLSearchParams(window.location.search)
    const mode = parseInt(params.has('m') ? params.get('m') : 0)
    if (params.has('t') && params.has('h') && params.has('c')) {
        document.querySelector('pre').innerText = params.get('c')
        document.querySelector('.title').innerText = params.get('h')
        document.querySelector('.time .inner').innerText = moment(parseInt(params.get('t'))).format('YYYY-MM-DD HH:mm:ss')
    }
    document.querySelector('.count .inner').innerText = document.querySelector('pre').innerText.length
    if (mode == 1) document.querySelector('article').innerHTML = markdown.toHTML(document.querySelector('pre').innerText)
</script>

</html>
'''


def show_index():
    return index_html.replace('<%SYSURL%/>', sys_url)


def show(title, content, time):
    return info_html.replace('<%TITLE%/>', title).replace('<%CONTENT%/>', content).replace('<%TIME%/>', time)


def show_param():
    return info_html.replace('<%TITLE%/>', '消息加载中, 请稍候').replace('<%CONTENT%/>', '').replace('<%TIME%/>', '')
