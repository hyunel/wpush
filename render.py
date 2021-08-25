html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>消息阅读 - WxPush</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">
    <style>
        body {
            background-color: #f5f8fa;
            padding: 0 16px;
            margin: 18px auto 0 auto;
            max-width: 768px;
        }
        .metabar > * {
            color: #868d91;
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
        }
        pre {
            white-space: normal;
            word-break: break-all;
        }
        .tittle {
            font-size: 22px;
            margin: 6px 0;
        }
        @media screen and (min-width: 768px) {
            .tittle {
                font-size: 28px;
            }
        }
    </style>
</head>
<body>
    <h1 class="tittle"><%TITTLE%/></h1>
    <div class="metabar">
        <div class="time"><i class="fa fa-clock-o"></i><span class="inner"><%TIME%/></span></div>
        <div class="count"><i class="fa fa-pencil"></i><span class="inner">0</span>字</div>
    </div>
    <article><pre><%CONTENT%/></pre></article>
</body>
<script src="https://cdn.jsdelivr.net/npm/js-base64@3.6.1/base64.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/moment@2.29.1/moment.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/markdown@0.5.0/lib/markdown.min.js"></script>

<script>
    const params = new URLSearchParams(window.location.search)
    const mode = parseInt(params.has('m') ? params.get('m') : 0)

    if(params.has('t') && params.has('h') && params.has('c')) {
        document.querySelector('pre').innerText=params.get('c')
        document.querySelector('.tittle').innerText=params.get('h')
        document.querySelector('.time .inner').innerText=moment(parseInt(params.get('t'))).format('YYYY-MM-DD hh:mm:ss')
    }

    document.querySelector('.count .inner').innerText=document.querySelector('pre').innerText.length
    // markdown mode
    if(mode == 1) document.querySelector('article').innerHTML=markdown.toHTML(document.querySelector('pre').innerText)
</script>
</html>'''


# 这里可能会有效率问题, 不值得上模板渲染引擎了, 直接简单替换
def show(tittle, content, time):
    return html.replace('<%TITTLE%/>', tittle).replace('<%CONTENT%/>', content).replace('<%TIME%/>', time)


def show_param():
    return html.replace('<%TITTLE%/>', '消息加载中, 请稍候').replace('<%CONTENT%/>', '').replace('<%TIME%/>', '')

