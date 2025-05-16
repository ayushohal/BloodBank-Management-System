const chatbotHTML = `
    <button onclick="toggleChatbot()" style="position: fixed; bottom: 20px; right: 20px; padding: 12px 18px; background-color: #e63946; color: white; border: none; border-radius: 30px; font-size: 16px;"> 
        Chat with us
    </button>
    
    <!-- Chatbot Modal -->
    <div id="chatbot-modal" style="display: none; position: fixed; bottom: 80px; right: 20px; width: 320px; height: 400px; background: white; border: 1px solid #ccc; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column;">
        <div style="background-color: #e63946; color: white; padding: 10px; text-align: center; font-weight: bold;">
            BloodBank Assistant
        </div>
        <div id="chat-window" style="flex: 1; padding: 10px; overflow-y: auto; font-size: 14px;">
            <div><strong>Assistant:</strong> Hi! Ask me anything about donors, inventory, or donations.</div>
        </div>
        <div style="display: flex; border-top: 1px solid #ddd;">
            <input type="text" id="chat-input-modal" placeholder="Type your message..." style="flex: 1; border: none; padding: 10px;" onkeydown="handleEnter(event)">
            <button onclick="sendMessage()" style="background-color: #e63946; color: white; border: none; padding: 10px 15px;">Send</button>
        </div>
    </div>
`;

document.body.insertAdjacentHTML("beforeend", chatbotHTML);

function toggleChatbot() {
    const modal = document.getElementById('chatbot-modal');
    modal.style.display = modal.style.display === 'none' ? 'flex' : 'none';
}

function handleEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    const inputField = document.getElementById("chat-input-modal");
    const chatWindow = document.getElementById("chat-window");
    const userMessage = inputField.value.trim();
    if (!userMessage) return;

    const userDiv = document.createElement("div");
    userDiv.innerHTML = `<strong>You:</strong> ${userMessage}`;
    chatWindow.appendChild(userDiv);

    inputField.value = "";

    chatWindow.scrollTop = chatWindow.scrollHeight;

    fetch("/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        const botDiv = document.createElement("div");
        botDiv.innerHTML = `<strong>Assistant:</strong> ${data.response}`;
        chatWindow.appendChild(botDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    })
    .catch(() => {
        const errorDiv = document.createElement("div");
        errorDiv.innerHTML = `<strong>Assistant:</strong> Something went wrong.`;
        chatWindow.appendChild(errorDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    });
}
