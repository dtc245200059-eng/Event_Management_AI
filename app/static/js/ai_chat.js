/**
 * Floating RAG AI Chatbot Widget Frontend Controller.
 */

document.addEventListener('DOMContentLoaded', () => {
    const chatBtn = document.getElementById('aiChatToggleBtn');
    const chatWindow = document.getElementById('aiChatWindow');
    const closeBtn = document.getElementById('aiChatCloseBtn');
    const sendBtn = document.getElementById('aiChatSendBtn');
    const inputField = document.getElementById('aiChatInput');
    const messagesContainer = document.getElementById('aiChatMessages');
    const quickPrompts = document.querySelectorAll('.quick-prompt-btn');

    if (!chatBtn || !chatWindow) return;

    // Toggle Chat Window
    chatBtn.addEventListener('click', () => {
        chatWindow.classList.toggle('hidden');
        if (!chatWindow.classList.contains('hidden')) {
            inputField.focus();
        }
    });

    closeBtn.addEventListener('click', () => {
        chatWindow.classList.add('hidden');
    });

    // Send Message
    async function sendMessage(text) {
        const query = text || inputField.value.trim();
        if (!query) return;

        // Clear input
        if (!text) inputField.value = '';

        // Append User Message
        appendMessage(query, 'user');

        // Append Typing indicator
        const typingEl = appendTypingIndicator();
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        try {
            // Get event_id if present in page data attribute
            const eventId = document.body.dataset.eventId || null;

            const response = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: query,
                    event_id: eventId ? parseInt(eventId) : null
                })
            });

            const data = await response.json();
            typingEl.remove();

            if (data.success) {
                appendMessage(data.response, 'bot', data.mode);
            } else {
                appendMessage(data.message || 'Có lỗi xảy ra khi kết nối tới AI. Vui lòng thử lại sau.', 'bot');
            }
        } catch (error) {
            typingEl.remove();
            appendMessage('Không thể kết nối tới máy chủ AI. Vui lòng kiểm tra kết nối mạng!', 'bot');
        }

        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function appendMessage(text, sender, mode = null) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-msg ${sender}`;
        
        // Basic markdown formatting: bold, lists, links, linebreaks
        let formatted = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" class="btn btn-xs btn-primary-gradient px-2 py-1 my-1 text-decoration-none d-inline-block text-white" target="_self">$1</a>')
            .replace(/\n- /g, '<br>• ')
            .replace(/\n\+ /g, '<br>&nbsp;&nbsp;+ ')
            .replace(/\n/g, '<br>');

        if (mode === 'mock') {
            formatted += '<div style="font-size: 0.7rem; color: #f59e0b; margin-top: 4px;">⚡ (Phản hồi qua Local Smart RAG Engine)</div>';
        }

        msgDiv.innerHTML = formatted;
        messagesContainer.appendChild(msgDiv);
        return msgDiv;
    }

    function appendTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-msg bot typing-indicator';
        typingDiv.innerHTML = '<span>🤖 AI đang tra cứu dữ liệu...</span>';
        messagesContainer.appendChild(typingDiv);
        return typingDiv;
    }

    // Event listeners
    sendBtn.addEventListener('click', () => sendMessage());
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    quickPrompts.forEach(btn => {
        btn.addEventListener('click', () => {
            const promptText = btn.dataset.prompt;
            sendMessage(promptText);
        });
    });
});
