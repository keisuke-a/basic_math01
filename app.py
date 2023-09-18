pip3 install langchain
#pip install openai

# 以下を「app.py」に書き込み
import streamlit as st
import openai

# langchian関連の関数を読み込み
import os

#下記のどちらかが必要
#openai.api_key = st.secrets.OpenAIAPI.openai_api_key
os.environ["OPENAI_API_KEY"] = st.secrets.OpenAIAPI.openai_api_key

#langchain関連のモジュールを読み込み
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory

llm = OpenAI(model_name="text-davinci-003", temperature=0.2)
tool_names = ["llm-math"]
tools = load_tools(tool_names, llm=llm)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

#system_prompt = """
#あなたは優秀なインド料理研究家です。
#限られた食材や時間で、様々な料理のレシピを提案することができます。
#どんな料理を指定されても、インド風のレシピとして提案します。
#あなたの役割はインド風のレシピを考えることなので、例えば以下のような料理以外ことを聞かれても、絶対に答えないでください。

#* 旅行
#* 芸能人
#* 映画
#* 科学
#* 歴史
#"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

#    response = openai.ChatCompletion.create(
#        model="gpt-3.5-turbo",
#        messages=messages
#    )  

#    bot_message = response["choices"][0]["message"]
    bot_message = agent.predict(messages)
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("数字の計算.bot")
st.write("計算問題を出してください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

#　チャットログを表示する
if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "👤"
        if message["role"]=="assistant":
            speaker="👱‍♂️"

        st.write(speaker + ": " + message["content"])
