/**
 * Economics Teaching Assistant Chatbot
 */

class EconChatbot {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || '/api/chat/';
        this.topicContext = options.topicContext || null;
        this.messages = [];
        this.isOpen = false;
        this.isLoading = false;

        this.init();
    }

    init() {
        this.container = document.getElementById('chatbot-container');
        if (!this.container) return;

        this.toggleBtn = document.getElementById('chatbot-toggle');
        this.closeBtn = document.getElementById('chatbot-close');
        this.messagesContainer = document.getElementById('chatbot-messages');
        this.input = document.getElementById('chatbot-input');
        this.sendBtn = document.getElementById('chatbot-send');
        this.form = document.getElementById('chatbot-form');

        this.bindEvents();
        this.addWelcomeMessage();
    }

    bindEvents() {
        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', () => this.toggle());
        }

        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }

        if (this.form) {
            this.form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendMessage();
            });
        }

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        this.container.classList.add('open');
        this.isOpen = true;
        this.input?.focus();
    }

    close() {
        this.container.classList.remove('open');
        this.isOpen = false;
    }

    addWelcomeMessage() {
        const welcomeText = `Hello! I'm your economics teaching assistant. I can help you understand inflation and related concepts from multiple schools of thought.

Ask me anything about:
• What different schools say about inflation
• How to compare economic perspectives
• Specific concepts like NAIRU, cost-push, or the Phillips curve
• Historical inflation episodes

What would you like to explore?`;

        this.addMessage('assistant', welcomeText);
    }

    addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${role}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = this.formatMessage(content);

        messageDiv.appendChild(contentDiv);

        if (role === 'assistant') {
            const tierBadge = document.createElement('span');
            tierBadge.className = 'message-tier';
            tierBadge.textContent = 'AI Generated';
            messageDiv.appendChild(tierBadge);
        }

        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatMessage(content) {
        // Use marked.js for proper markdown rendering
        if (typeof marked !== 'undefined') {
            // Configure marked for safe rendering
            marked.setOptions({
                breaks: true,  // Convert \n to <br>
                gfm: true,     // GitHub Flavored Markdown
            });
            return marked.parse(content);
        }
        // Fallback to basic formatting if marked isn't loaded
        return content
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            .replace(/^• /gm, '&bull; ')
            .replace(/^- /gm, '&bull; ');
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    async sendMessage() {
        const content = this.input.value.trim();
        if (!content || this.isLoading) return;

        // Add user message
        this.messages.push({ role: 'user', content });
        this.addMessage('user', content);

        // Clear input
        this.input.value = '';

        // Show loading
        this.setLoading(true);

        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    messages: this.messages,
                    topic_context: this.topicContext,
                }),
            });

            const data = await response.json();

            if (data.success) {
                this.messages.push({ role: 'assistant', content: data.response });
                this.addMessage('assistant', data.response);
            } else {
                this.addMessage('assistant', `Sorry, I encountered an error: ${data.error}`);
            }
        } catch (error) {
            console.error('Chatbot error:', error);
            this.addMessage('assistant', 'Sorry, I couldn\'t connect to the server. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }

    setLoading(loading) {
        this.isLoading = loading;
        this.sendBtn.disabled = loading;
        this.input.disabled = loading;

        if (loading) {
            this.sendBtn.innerHTML = '<span class="loading-dots">...</span>';
        } else {
            this.sendBtn.innerHTML = 'Send';
        }
    }

    getCSRFToken() {
        // Get CSRF token from cookie
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Initialize chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const chatbotContainer = document.getElementById('chatbot-container');
    if (chatbotContainer) {
        const topicContext = chatbotContainer.dataset.topicContext || null;
        window.econChatbot = new EconChatbot({
            topicContext: topicContext,
        });
    }
});
