# sast2023 word game

## 环境配置

详见 `requirements.txt`

## 使用设置

约定以下参数：

```

--file  -f  接文章的路径
--id    -i 可选参数，如果想要指定文章就给出在对应 JSON 文件中的编号，下标从 0 开始

```

文章使用 JSON 存储，的格式如下：

```json
{
    "language": "zh",
    "articles": [
        {
            "title": "...",
            "article": "...",
            "hints": [...]
        },
		...
}

```



## 游戏功能

* 使用 Streamlit 实现了 GUI
* 增加了一些新的题目
* 如果不指定具体的文章编号，用户将以随机的顺序不重复遍历完 JSON 文件中所有的文章
* 支持下载用户生成的内容
