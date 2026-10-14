/**
 * Floating RAG AI Chatbot Widget Frontend Controller.
 * Features: Marked.js Markdown & Table rendering, multi-turn history, sessionStorage persistence.
 */

document.addEventListener('DOMContentLoaded', () => {
    const chatBtn = document.getElementById('aiChatToggleBtn');
    const chatWindow = document.getElementById('aiChatWindow');
    const closeBtn = document.getElementById('aiChatCloseBtn');
    const sendBtn = document.getElementById('aiChatSendBtn');
    const inputField = document.getElementById('aiChatInput');
    const messagesContainer = document.getElementById('aiChatMessages');
    const quickPrompts = document.querySelectorAll('.quick-prompt-btn');

    if (!chatWindow) return;

    // Multi-turn conversation history
    let floatingHistory = [];
    const STORAGE_KEY = 'eventai_floating_chat';

    // Load from sessionStorage if available
    try {
        const saved = sessionStorage.getItem(STORAGE_KEY);
        if (saved) {
            floatingHistory = JSON.parse(saved);
            if (floatingHistory.length > 0) {
                // Re-render saved messages
                messagesContainer.innerHTML = '';
                floatingHistory.forEach(item => {
                    renderMessage(item.content, item.role === 'user' ? 'user' : 'bot', item.mode);
                });
            }
        }
    } catch (e) {
        console.warn('Could not restore chat history:', e);
    }

    function saveHistory() {
        try {
            sessionStorage.setItem(STORAGE_KEY, JSON.stringify(floatingHistory.slice(-20)));
        } catch (e) {}
    }

    const chatBackdrop = document.getElementById('aiChatBackdrop');

    function openChatWindow() {
        if (typeof window.closeMobileDrawer === 'function') {
            window.closeMobileDrawer();
        }
        chatWindow.classList.remove('hidden');
        if (chatBackdrop) {
            chatBackdrop.classList.add('open', 'active');
        }
        document.body.classList.add('mobile-chat-open');
        setTimeout(() => {
            if (inputField) inputField.focus();
            if (messagesContainer) messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 80);
    }

    function closeChatWindow() {
        chatWindow.classList.add('hidden');
        if (chatBackdrop) {
            chatBackdrop.classList.remove('open', 'active');
        }
        document.body.classList.remove('mobile-chat-open');
    }

    // Expose globally so Mobile Bottom Navigation tab can open it
    window.openEventAIChat = openChatWindow;
    window.closeEventAIChat = closeChatWindow;

    // Toggle Chat Window via button
    if (chatBtn) {
        chatBtn.addEventListener('click', () => {
            if (chatWindow.classList.contains('hidden')) {
                openChatWindow();
            } else {
                closeChatWindow();
            }
        });
    }

    if (closeBtn) closeBtn.addEventListener('click', closeChatWindow);
    if (chatBackdrop) {
        chatBackdrop.addEventListener('click', closeChatWindow);
    }

    // Escape key closes AI chat window
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !chatWindow.classList.contains('hidden')) {
            closeChatWindow();
        }
    });

    // Send Message
    async function sendMessage(text) {
        const query = text || inputField.value.trim();
        if (!query) return;

        // Clear input
        if (!text) inputField.value = '';

        // Append User Message to UI & History
        renderMessage(query, 'user');
        floatingHistory.push({ role: 'user', content: query });
        saveHistory();

        // Append Typing indicator
        const typingEl = appendTypingIndicator();
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        try {
            // Get event_id if present in page data attribute
            const eventId = document.body.dataset.eventId || null;

            // Prepare conversation history (last 6 turns)
            const historyPayload = floatingHistory.slice(-6).map(h => ({
                role: h.role,
                content: h.content
            }));

            const response = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: query,
                    event_id: eventId ? parseInt(eventId) : null,
                    history: historyPayload
                })
            });

            const data = await response.json();
            typingEl.remove();

            if (data && data.success && data.response) {
                renderMessage(data.response, 'bot', data.mode);
                floatingHistory.push({ role: 'model', content: data.response, mode: data.mode });
                saveHistory();
            } else {
                renderMessage(data.message || 'Không thể lấy phản hồi từ AI vào lúc này. Vui lòng thử lại sau!', 'bot');
            }
        } catch (error) {
            console.error('EventAI Chatbot Error:', error);
            typingEl.remove();
            renderMessage('Hệ thống đang bận hoặc gián đoạn kết nối. Vui lòng gửi lại câu hỏi sau giây lát!', 'bot');
        }

        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function formatMarkdown(rawInput) {
        if (!rawInput && rawInput !== 0) return '';

        let rawText = rawInput;

        // 1. Guard against direct Objects or Arrays
        if (typeof rawText !== 'string') {
            try {
                if (Array.isArray(rawText)) {
                    if (rawText.length === 0) {
                        return `<div class="empty-events-state text-center p-3 my-2 rounded-3" style="background: var(--surface-secondary); border: 1px dashed var(--border-regular);">
                            <i class="fa-regular fa-calendar-xmark fs-4 mb-1 text-primary opacity-75 d-block"></i>
                            <strong class="d-block small mb-1" style="color: var(--text-primary);">Không có sự kiện nào!</strong>
                            <span class="small text-muted" style="font-size: 0.72rem;">Hiện chưa có sự kiện miễn phí phù hợp.</span>
                        </div>`;
                    }
                    rawText = rawText.map(item => typeof item === 'object' && item !== null ? `- [${item.title || 'Sự kiện'}](/events/${item.id || ''})` : `- ${String(item)}`).join('\n');
                } else if (typeof rawText === 'object' && rawText !== null) {
                    rawText = rawText.answer || rawText.response || rawText.content || rawText.message || '';
                } else {
                    rawText = String(rawText);
                }
            } catch (e) {
                rawText = '';
            }
        }

        // 2. Sanitize against '[object Object]', 'undefined', 'null', 'NaN'
        if (rawText === '[object Object]' || rawText.includes('[object Object]undefined') || rawText.includes('[object Object]')) {
            rawText = rawText.replace(/\[object Object\]undefined/g, '')
                             .replace(/\[object Object\]/g, '');
            if (!rawText.trim()) {
                return `<div class="empty-events-state text-center p-3 my-2 rounded-3" style="background: var(--surface-secondary); border: 1px dashed var(--border-regular);">
                    <i class="fa-regular fa-calendar-xmark fs-4 mb-1 text-primary opacity-75 d-block"></i>
                    <strong class="d-block small mb-1" style="color: var(--text-primary);">Không có sự kiện nào!</strong>
                    <span class="small text-muted" style="font-size: 0.72rem;">Hiện chưa có sự kiện miễn phí phù hợp.</span>
                </div>`;
            }
        }

        const emptyStateHtml = `<div class="empty-events-state text-center p-3 my-2 rounded-3" style="background: var(--surface-secondary); border: 1px dashed var(--border-regular);">
            <i class="fa-regular fa-calendar-xmark fs-4 mb-1 text-primary opacity-75 d-block"></i>
            <strong class="d-block small mb-1" style="color: var(--text-primary);">Không có sự kiện nào!</strong>
            <span class="small text-muted" style="font-size: 0.72rem;">Hiện chưa có sự kiện miễn phí phù hợp.</span>
        </div>`;

        // 3. Render using Marked.js if available
        if (window.marked && typeof window.marked.parse === 'function') {
            try {
                let html = window.marked.parse(rawText, { gfm: true, breaks: true });

                // Detect empty table
                const emptyTableRegex = /<table>\s*<thead>[\s\S]*?<\/thead>\s*(?:<tbody>\s*<\/tbody>)?\s*<\/table>/gi;
                html = html.replace(emptyTableRegex, emptyStateHtml);

                // Wrap tables
                html = html.replace(/<table>/gi, '<div class="table-responsive my-2"><table class="table table-hover table-bordered table-sm align-middle mb-0" style="font-size: 0.78rem; background: var(--surface-primary); color: var(--text-primary); border-color: var(--border-hairline);">');
                html = html.replace(/<\/table>/gi, '</table></div>');

                // Style action buttons / links
                html = html.replace(/<a href="([^"]+)">([^<]*(?:👉|Đặt vé|Xem chi tiết|Đăng ký)[^<]*)<\/a>/gi, '<a href="$1" class="btn btn-xs btn-primary rounded-pill px-3 py-1 my-1 text-decoration-none d-inline-block text-white" target="_self">$2</a>');

                return html;
            } catch (e) {
                console.warn('Marked parsing error, falling back:', e);
            }
        }

        // 4. Fallback lightweight regex formatting
        let out = rawText
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" class="btn btn-xs btn-primary rounded-pill px-3 py-1 my-1 text-decoration-none d-inline-block text-white" target="_self">$1</a>')
            .replace(/\n- /g, '<br>• ')
            .replace(/\n\+ /g, '<br>&nbsp;&nbsp;+ ')
            .replace(/\n/g, '<br>');

        return out;
    }

    function renderMessage(text, sender, mode = null) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-msg ${sender}`;

        let formatted = formatMarkdown(text);

        if (mode === 'live') {
            formatted += '<div style="font-size: 0.68rem; color: #10b981; margin-top: 4px;"><i class="fa-solid fa-cloud me-1"></i>Gemini 3.6 Flash Live</div>';
        } else if (mode === 'mock') {
            formatted += '<div style="font-size: 0.68rem; color: #f59e0b; margin-top: 4px;"><i class="fa-solid fa-database me-1"></i>Local Grounded RAG Engine</div>';
        }

        msgDiv.innerHTML = formatted;
        messagesContainer.appendChild(msgDiv);
        return msgDiv;
    }

    function appendTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-msg bot typing-indicator';
        typingDiv.innerHTML = '<span><i class="fa-solid fa-circle-notch fa-spin me-1"></i> AI đang xử lý & tra cứu dữ liệu...</span>';
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
