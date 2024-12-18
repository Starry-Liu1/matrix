from flask import Flask, render_template, request, jsonify, session
import json
import os
from my_agents import emotion_agent, topic_agent, user_profile_agent, response_agent

app = Flask(__name__)

# 定义保存历史对话的文件路径
HISTORY_FILE_PATH = "chat_history.json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"reply": "未接收到消息，请重试。"}), 400

    # 使用多Agent获取情感和主题信息
    detected_emotion = emotion_agent.detect_emotion(user_input)
    detected_topic = topic_agent.detect_topic(user_input)

    # 更新用户画像
    user_profile_agent.update_profile(detected_emotion, detected_topic)

    # 使用LLM生成基于情感和主题的响应
    bot_response = response_agent.generate_response(user_input, detected_emotion, detected_topic)
    response_agent.history.append({"role": "system", "content": bot_response})
    return jsonify({"reply": bot_response})

# 新增API路由：清空历史记录
@app.route("/api/clear-history", methods=["POST"])
def clear_history():
    response_agent.history = []  # 清空历史记录
    return jsonify({"status": "success", "message": "历史记录已清空"})

# 新增API路由：保存历史对话
@app.route("/api/save-history", methods=["POST"])
def save_history():
    # 获取当前的历史记录
    history = response_agent.history

    # 将历史记录保存到JSON文件中
    try:
        with open(HISTORY_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
        return jsonify({"status": "success", "message": "历史对话已保存"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"保存历史对话时出错: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)