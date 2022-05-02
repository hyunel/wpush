import config

sys_url = config.get('sys_url')
index_html = '''
<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://unpkg.com/vue@next"></script>
    <link rel="stylesheet" href="https://unpkg.com/element-plus/dist/index.css">
    <script src="https://unpkg.com/element-plus"></script>
    <link rel="icon" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.1.1/svgs/regular/comments.svg">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">
    <title>WPUSH</title>
</head>

<body>
    <div id="app">
        <!-- 发送消息 -->
        <section>
            <div class="con2">
                <div class="form">
                    <h2>WPUSH</h2>
                    <div>
                        <el-form ref="elForm" :model="formData" :rules="rules" size="default" label-width="100px">
                            <el-form-item label-width="0" prop="type">
                                <el-select v-model="formData.type" placeholder="消息类型" :style="{width: '100%'}"
                                    :disabled="disabled">
                                    <el-option v-for="(item, index) in typeOptions" :key="index" :label="item.label"
                                        :value="item.value" :disabled="item.disabled" @click="clickOp(item.value)">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label-width="0" prop="secret">
                                <el-input v-model=" formData.secret" placeholder="秘钥" clearable show-password
                                    :style="{width: '100%'}" :disabled="disabled">
                                </el-input>
                            </el-form-item>

                            <el-form-item label-width="0" prop="pic" v-show="type =='news'">
                                <el-input v-model="formData.pic" placeholder="图片链接" clearable :style="{width: '100%'}"
                                    :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label-width="0" prop="url" v-show="type =='textcard'||type=='news'">
                                <el-input v-model="formData.url" placeholder="跳转链接" clearable :style="{width: '100%'}"
                                    :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label-width="0" prop="title" v-show="type =='textcard'||type=='news'">
                                <el-input v-model="formData.title" placeholder="标题" clearable :style="{width: '100%'}"
                                    :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label-width="0" prop="summary" v-show="type =='textcard'||type=='news'">
                                <el-input v-model="formData.summary" placeholder="摘要" clearable :style="{width: '100%'}"
                                    :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item label-width="0" prop="content">
                                <el-input v-model="formData.content" type="textarea" placeholder="内容"
                                    :autosize="{minRows: 4, maxRows: 4}" :style="{width: '100%'}" :disabled="disabled">
                                </el-input>
                            </el-form-item>
                            <el-form-item size="large" class="btn">
                                <el-button type="primary" @click="submitForm" round size="large" :loading="disabled">
                                    {{submitInfo}}
                                </el-button>
                                <el-button @click="resetForm" round size="large" :disabled="disabled">重置</el-button>
                            </el-form-item>
                        </el-form>
                    </div>
                </div>
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


    .con2 {
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

    .form h2 {
        position: relative;
        color: #fff;
        font-size: 24px;
        font-weight: 600;
        letter-spacing: 5px;
        margin-bottom: 30px;
        cursor: pointer;
    }

    .el-input__wrapper,
    .el-textarea__inner {
        border-radius: 20px !important;
    }

    .el-message-box {
        width: 300px;
    }

    .btn .el-form-item__content {
        margin-left: 0px !important
    }
</style>
<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
<script>
    const App = {
        data() {
            return {
                submitInfo: "发送",
                disabled: false,
                type: "text",
                link: "",
                formData: {
                    secret: undefined,
                    title: undefined,
                    summary: undefined,
                    content: undefined,
                    pic: undefined,
                    url: undefined,
                    type: "text",
                },
                rules: {
                    secret: [{
                        required: true,
                        message: '秘钥',
                        trigger: 'blur'
                    }],
                    type: [{
                        required: true,
                        message: '消息类型',
                        trigger: 'change'
                    }],
                    pic: [{
                        required: false,
                        message: '图片链接',
                        trigger: 'blur'
                    }],
                    url: [{
                        required: false,
                        message: '跳转链接',
                        trigger: 'blur'
                    }],
                    title: [{
                        required: false,
                        message: '内容',
                        trigger: 'blur'
                    }],
                    summary: [{
                        required: false,
                        message: '摘要',
                        trigger: 'blur'
                    }],
                    content: [{
                        required: true,
                        message: '内容',
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
                    "label": "markdown",
                    "value": "markdown"
                }, {
                    "label": "图文消息",
                    "value": "news"
                }],
            }
        },

        methods: {
            clickOp(item) {
                this.type = item
                if (item == "news" || item == "textcard") {
                    this.rules.title[0].required = true
                } else {
                    this.rules.title[0].required = false
                }
            },
            submitForm() {
                this.disabled = true
                this.submitInfo = "发送中"
                let content = this.formData.content
                this.formData.content = decodeURIComponent(content)
                this.$refs['elForm'].validate(valid => {
                    if (!valid) {
                        this.disabled = false
                        this.submitInfo = "发送"
                        this.showErrorConfirm("校验失败，请完整填写参数")
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
                            this.submitInfo = "发送"
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
                            this.submitInfo = "发送"
                            this.showErrorConfirm("消息发送失败，请稍后再试~")
                        })
                    }
                })
            },
            resetForm() {
                this.$refs['elForm'].resetFields()
                this.type = "text"
            },
            showLinkConfirm(msg) {
                this.$confirm(msg, '提示', {
                    confirmButtonText: '前往',
                    cancelButtonText: '返回',
                    type: 'success'
                }).then(() => {
                    window.open(this.link, "_self")
                }).catch(() => {
                })
            },
            showSuccessConfirm(msg) {
                this.$confirm(msg, '提示', {
                    cancelButtonText: '返回',
                    showConfirmButton: false,
                    type: 'success'
                })
            },
            showErrorConfirm(msg) {
                this.$confirm(msg, '提示', {
                    cancelButtonText: '返回',
                    showConfirmButton: false,
                    type: 'error'
                })
            }
        }
    }
    const app = Vue.createApp(App);
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
    <link rel="icon" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.1.1/svgs/regular/comments.svg">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">
    <title>WPUSH</title>
</head>

<body>
    <div id="app">
        <!-- 显示消息 -->
        <section>
            <div class="con1">
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

    .con1 {
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
<script src="https://cdn.jsdelivr.net/npm/js-base64@3.6.1/base64.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/moment@2.29.1/moment.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/markdown@0.5.0/lib/markdown.min.js"></script>
<script>
    const params = new URLSearchParams(window.location.search)
    const mode = parseInt(params.has('m') ? params.get('m') : 0)
    if (params.has('t') && params.has('h') && params.has('c')) {
        document.querySelector('pre').innerText = params.get('c')
        document.querySelector('.title').innerText = params.get('h')
        document.querySelector('.time .inner').innerText = moment(parseInt(params.get('t'))).format('YYYY-MM-DD hh:mm:ss')
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
