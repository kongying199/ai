import os

os.environ["OPENAI_API_KEY"] = ''

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4")



from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

model.invoke(messages)