from openai import OpenAI
from transformers import pipeline
import json
import os
import nltk


# OpenAI API Key
#openai.api_key = "sk-yTIpknH80e6eTLshCety8f2ltHhjzYJbZdEYpALR2u8Zk4m3"
client = OpenAI(
        api_key="sk-yTIpknH80e6eTLshCety8f2ltHhjzYJbZdEYpALR2u8Zk4m3",
        base_url="https://api.chatanywhere.com.cn/v1",
    )
# 初始化情感分析器
class EmotionAgent:
    def __init__(self):
        self.emotion_labels = ["高兴", "悲伤", "愤怒", "恐惧", "惊讶", "平静"]

    def detect_emotion(self, text):
        prompt = f"请分析以下句子的情感，并在“高兴”、“悲伤”、“愤怒”、“恐惧”、“惊讶”、“平静”六种情感中选择最符合的一种。\n\n句子：{text}\n\n情感："

        response = client.chat.completions.create(
            messages = [
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt},
            ],
            model="gpt-4o-mini",
            max_tokens=10,
            temperature=0.1,


        )

        emotion = response.choices[0].message.content
        return emotion


class TopicAgent:
    def detect_topic(self, text):
        prompt = f"请分析以下句子的主题，选择最合适的主题分类：如“天气”、“新闻”、“健康”、”体育“、“生活”或“其他”。\n\n句子：{text}\n\n主题："

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": prompt},
            ],
            model="gpt-4o-mini",
            max_tokens=10,
            temperature=0.1,
        )

        topic = response.choices[0].message.content
        return topic


class UserProfileAgent:
    def __init__(self):
        self.user_profile = {"emotion_history": [], "topics": []}

    def update_profile(self, emotion, topic):
        self.user_profile["emotion_history"].append(emotion)
        self.user_profile["topics"].append(topic)


class ResponseAgent:

    def __init__(self):
        self.history=[]
    def generate_response(self, user_input, emotion, topic):
        # 利用LLM生成响应，将情感和主题作为上下文提供给模型
        prompt = (
            f"用户的输入：{user_input}\n\n"
            f"检测到的情感：{emotion}\n"
            f"检测到的主题：{topic}\n\n"
            "请基于用户的情感和主题以及之前的交互历史生成一个友好的回复，以表达关心和支持，帮助用户感到被理解和陪伴。\n\n回复："
        )
        self.history.append({"role": "user", "content": prompt})
        print(self.history)
        response = client.chat.completions.create(
            messages=self.history,
            model="gpt-4o-mini",
            max_tokens=1024,
            temperature=0.1,

        )

        bot_response = response.choices[0].message.content
        return bot_response


class ConversationContext:
    def __init__(self):
        self.history = []

    def add_to_history(self, user_input, bot_response):
        self.history.append({"user": user_input, "bot": bot_response})
        if len(self.history) > 5:
            self.history.pop(0)

    def get_context(self):
        context = "\n".join([f"User: {item['user']}\nBot: {item['bot']}" for item in self.history])
        return context
# 实例化 agents
emotion_agent = EmotionAgent()
topic_agent = TopicAgent()
user_profile_agent = UserProfileAgent()
response_agent = ResponseAgent()