// 登录页面逻辑
const loginPage = document.getElementById("login-page");
const mainPage = document.getElementById("main-page");
const loginForm = document.getElementById("login-form");
const usernameInput = document.getElementById("username");
const genderInput = document.getElementById("gender");
const ageInput = document.getElementById("age");
const currentUserDisplay = document.getElementById("current-user");
const currentGenderDisplay = document.getElementById("current-gender");
const currentAgeDisplay = document.getElementById("current-age");

loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    // 获取用户输入的信息
    const username = usernameInput.value.trim();
    const gender = genderInput.value;
    const age = ageInput.value.trim();

    if (username === "" || gender === "" || age === "") {
        alert("请完整填写信息！");
        return;
    }

    // 设置用户信息到主页面
    currentUserDisplay.textContent = username;
    currentGenderDisplay.textContent = gender;
    currentAgeDisplay.textContent = age;

    // 切换到主页面
    loginPage.style.display = "none";
    mainPage.style.display = "flex";
});

function displayMessage(message, type) {
    const chatbox = document.getElementById("chatbox");
    const messageElement = document.createElement("div");
    messageElement.className = "message " + (type === "user" ? "user-message" : "bot-message");
    messageElement.textContent = message;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function sendMessage() {
    const messageInput = document.getElementById("message");
    const message = messageInput.value.trim();
    if (message === "") return;

    displayMessage(message, "user");
    messageInput.value = "";

    // 向后端发送用户输入
    fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        displayMessage(data.reply, "bot");
    })
    .catch(error => {
        console.error("Error:", error);
        displayMessage("抱歉，出现了一些问题，请稍后再试。", "bot");
    });
}

// 新增功能：开始新的对话
function startNewConversation() {
    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML = ""; // 清空聊天记录

    // 向后端发送请求，清空历史记录
    fetch("/api/clear-history", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // 输出成功信息
    })
    .catch(error => {
        console.error("Error clearing history:", error);
    });
}

// 新增功能：保存历史对话
function saveHistory() {
    const chatbox = document.getElementById("chatbox");
    const messages = chatbox.innerHTML; // 获取当前聊天记录的HTML内容

    // 向后端发送请求，保存历史记录
    fetch("/api/save-history", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ history: messages })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // 弹出保存成功的提示
    })
    .catch(error => {
        console.error("Error saving history:", error);
        alert("保存历史记录时出错，请稍后再试。");
    });
}

// 将新对话按钮绑定到点击事件
document.getElementById("new-conversation-button").addEventListener("click", startNewConversation);

// 将保存历史对话按钮绑定到点击事件
document.getElementById("save-history-button").addEventListener("click", saveHistory);