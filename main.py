import argparse
import json
import random
from pathlib import Path
import streamlit as st
import copy

def parser_data():
    """
    从命令行读取用户参数
    做出如下约定：
    1. -f 为必选参数，表示输入题库文件
    ...

    :return: 参数
    """
    parser = argparse.ArgumentParser(
        prog="Word filling game",
        description="A simple game",
        allow_abbrev=True
    )

    parser.add_argument("-f", "--file", help="题库文件", required=True)
    parser.add_argument("-i", "--id", help="指定文章，需要给出文章在题库文件中的编号，下标从 0 开始", required=False)
    # TODO: 添加更多参数
    
    args = parser.parse_args()
    return args



def read_articles(filename):
    """
    读取题库文件

    :param filename: 题库文件名

    :return: 一个字典，题库内容
    """
    with open(filename, 'r', encoding="utf-8") as f:
        data = json.load(f)
        # TODO: 用 json 解析文件 f 里面的内容，存储到 data 中
    return data



def get_inputs(hints, args):
    """
    获取用户输入

    :param hints: 提示信息

    :return: 用户输入的单词
    """
    keys = []
    # submit_button = 0
    with st.form(key='my_form'):
        for i in range(len(hints)):
            keys.append(st.text_input(label="第"+str(i+1)+"个词，提示为"+hints[i]))
        submit_button = st.form_submit_button(label='Submit')
        if args.id == None:
            regenerate_button = st.form_submit_button(label='Regenerate')
        else:
            regenerate_button = 0
    return (keys, submit_button, regenerate_button)


def replace(article, keys):
    """
    替换文章内容

    :param article: 文章内容
    :param keys: 用户输入的单词

    :return: 替换后的文章内容

    """
    result = copy.deepcopy(article)
    article_with_color = copy.deepcopy(article["article"])
    # print(article)
    for i in range(len(keys)):
        # article["article"] = article["article"].replace(f"{{{{{i+1}}}}}", "\033[31m"+keys[i]+"\033[0m")
        article_with_color = article_with_color.replace(f"{{{{{i+1}}}}}", ":red["+keys[i]+"]")
        result["article"] = result["article"].replace(f"{{{{{i+1}}}}}", keys[i])

    return (result, article_with_color)

@st.cache_data
def get_article(id, articles, timestep):
    if id != None:
        try:
            article = articles[int(id)]
        except IndexError:
            st.error("初始化错误: 不存在您指定的文章\n 请重新启动该程序")
            exit(0)
    else:
        try:
            article = articles[timestep]
        except IndexError:
            st.error("已经做完所有的文章了！")
            exit(0)
    return article

def init(args, articles):
    if "time_step" not in st.session_state:
        st.session_state["time_step"] = "0"
    if "articles" not in st.session_state:
        if args.id == None:
            random.shuffle(articles)
        st.session_state["articles"] = articles

if __name__ == "__main__":
    args = parser_data()
    data = read_articles(args.file)
    articles = data["articles"]

    init(args, articles)
    articles = st.session_state["articles"]
        
    article = get_article(args.id, articles, int(st.session_state["time_step"]))
    
    # print(article)
    # TODO: 给出合适的输出，提示用户输入
    st.header("填词游戏")
    
    st.subheader("规则介绍:")
    st.markdown("""
                - 在后台中存储了一篇文章，但是这篇文章的若干个位置的词语
                - 现在会在你不知道文章的情况下给出这些空对应的解释，你需要填上一个对应的词语。
                - 填空完成后点击 Submit 按钮，看看你的文章有多欢乐！
                - 如果你想换一个文章，点击 Regenerate 重新随机生成一个文章（只有在命令行参数不指定文章 id 的情况下）
                """)
    
    (keys,submitted,regenerated) = get_inputs(article["hints"], args)
    # print(keys,submitted,regenerated)
    # TODO: 获取用户输入并进行替换
    
    (answer, answer_with_color) = replace(article, keys)
    # TODO: 给出结果
    if regenerated:
        time_step = int(st.session_state["time_step"])
        # print(st.session_state[""]time_step)
        time_step += 1
        st.session_state["time_step"] = str(time_step)
        st.experimental_rerun()
    print(st.session_state)
    if submitted or ("downloaded" in st.session_state and st.session_state["downloaded"] == 'True'):
        st.subheader(answer["title"])
        st.write(answer_with_color)
        st.session_state["download"] = 'False'
        
        user_article=answer["title"] + "\n" + answer["article"]
        
        def display_answer():
            st.session_state["downloaded"] = 'True'
            
        st.download_button(
            label="Download your article as .txt",
            data=user_article,
            file_name="Result-" + answer["title"] + ".txt",
            on_click = display_answer
        )


