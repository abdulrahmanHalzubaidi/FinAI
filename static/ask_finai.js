function updateFileName() {
    const fileInput = document.getElementById("file");
    const fileName = document.getElementById("fileName");
    fileName.textContent = fileInput.files.length > 0 ? fileInput.files[0].name : "Attach File";
}

function scrollToLatest() {
    const chatBox = document.getElementById("chat-box");
    chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
}

document.getElementById("chat-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById("file");
    const queryInput = document.getElementById("query");
    const chatBox = document.getElementById("chat-box");
    const query = queryInput.value.trim();

    queryInput.value = "";

    const formData = new FormData();
    if (fileInput.files.length > 0) {
        formData.append("file", fileInput.files[0]);
    }
    formData.append("query", query);

    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.textContent = query;
    chatBox.prepend(userMessage);
    scrollToLatest();

    const loadingMessage = document.createElement("div");
    loadingMessage.className = "message bot";
    loadingMessage.innerHTML = `
        <span>typing</span>
        <span class="typing-dots">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </span>`;
    chatBox.prepend(loadingMessage);
    scrollToLatest();

    try {
        const response = await fetch("/chat", { method: "POST", body: formData });
        const result = await response.json();
        loadingMessage.remove();

        const botMessage = document.createElement("div");
        botMessage.className = "message bot";
        botMessage.innerHTML = result.response || `<span>${result.error || "Unexpected error"}</span>`;
        chatBox.prepend(botMessage);
    } catch (error) {
        loadingMessage.remove();
        const errorMessage = document.createElement("div");
        errorMessage.className = "message bot";
        errorMessage.textContent = "Failed to fetch response.";
        chatBox.prepend(errorMessage);
    }
});