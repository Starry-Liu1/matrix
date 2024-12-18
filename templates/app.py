from flask import Flask, request, jsonify, render_template
from my_agents import emotion_agent, topic_agent, user_profile_agent, response_agent  # 引入定义的agents

app = Flask(__name__)


@app.route("/")
def index():
    # 渲染 templates 目录下的 index.html 文件
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    # 调用多Agent获取响应
    basic_emotion, detailed_emotion = emotion_agent.detect_emotion(user_input)
    topic = topic_agent.detect_topic(user_input)

    # 更新用户画像
    user_profile_agent.update_profile(basic_emotion, topic)

    # 生成并返回响应
    bot_response = response_agent.generate_response(user_input, basic_emotion, detailed_emotion, topic)
    response_agent.history.append(bot_response)
    return jsonify({"reply": bot_response})


if __name__ == "__main__":
    app.run(debug=True)
