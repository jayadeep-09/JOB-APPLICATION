document.addEventListener("DOMContentLoaded", function() {
    const chatBtn = document.getElementById('ai-chatbot-btn');
    const chatWindow = document.getElementById('ai-chatbot-window');
    const closeBtn = document.getElementById('close-chatbot');
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    
    const uploadZone = document.getElementById('upload-zone');
    const resumeInput = document.getElementById('resume-file');
    const dropText = document.getElementById('drop-text');
    const uploadingSpinner = document.getElementById('uploading-spinner');

    // Load history
    let historyLoaded = false;
    
    async function loadHistory() {
        if(historyLoaded) return;
        try {
            const res = await fetch('/chatbot/api/history/');
            const data = await res.json();
            if(data.history && data.history.length > 0) {
                // Clear initial message if history exists
                chatMessages.innerHTML = '';
                data.history.forEach(msg => {
                    appendMessage(msg.message, msg.is_bot);
                });
            }
            historyLoaded = true;
        } catch(e) {
            console.error("Failed to load history", e);
        }
    }

    // Toggle Window
    chatBtn.addEventListener('click', () => {
        chatWindow.classList.remove('d-none');
        chatWindow.classList.remove('closing');
        loadHistory();
        scrollToBottom();
    });

    closeBtn.addEventListener('click', () => {
        chatWindow.classList.add('closing');
        setTimeout(() => {
            chatWindow.classList.add('d-none');
        }, 250); // Matches animation duration
    });

    // Formatting Markdown (Basic)
    function formatMessage(text) {
        let html = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Handle basic lists if ai engine formats them
        return `<p>${html}</p>`;
    }

    // Appending Messages
    function appendMessage(text, isBot = false) {
        const div = document.createElement('div');
        div.className = `message ${isBot ? 'bot-message' : 'user-message'}`;
        div.innerHTML = formatMessage(text);
        chatMessages.appendChild(div);
        scrollToBottom();
    }

    function showTyping() {
        const div = document.createElement('div');
        div.className = 'message bot-message typing-msg';
        div.innerHTML = `<div class="typing-indicator"><span></span><span></span><span></span></div>`;
        chatMessages.appendChild(div);
        scrollToBottom();
    }

    function removeTyping() {
        const typingMsgs = document.querySelectorAll('.typing-msg');
        typingMsgs.forEach(el => el.remove());
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Send Chat Message
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if(!msg) return;

        appendMessage(msg, false);
        chatInput.value = '';
        showTyping();

        try {
            const formData = new FormData();
            formData.append('message', msg);
            const res = await fetch('/chatbot/api/chat/', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            removeTyping();
            
            if(data.success) {
                appendMessage(data.reply, true);
            } else {
                appendMessage("Sorry, I encountered an error. Please try again.", true);
            }
        } catch(e) {
            removeTyping();
            appendMessage("Network error. Could not connect to AI engine.", true);
        }
    });

    // Handle Upload
    uploadZone.addEventListener('click', () => resumeInput.click());
    
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });
    
    uploadZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
    });
    
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        if(e.dataTransfer.files.length) {
            resumeInput.files = e.dataTransfer.files;
            handleUpload();
        }
    });

    resumeInput.addEventListener('change', () => {
        if(resumeInput.files.length) {
            handleUpload();
        }
    });

    async function handleUpload() {
        const file = resumeInput.files[0];
        if(!file) return;

        dropText.classList.add('d-none');
        uploadingSpinner.classList.remove('d-none');

        const formData = new FormData();
        formData.append('resume', file);

        try {
            const res = await fetch('/chatbot/api/upload/', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            
            uploadingSpinner.classList.add('d-none');
            dropText.classList.remove('d-none');
            
            if(data.success) {
                appendMessage(`Successfully uploaded and analyzed **${file.name}**. I found skills like ${data.analysis.skills.slice(0,3).join(', ')}. Ask me about your ATS score or job suggestions!`, true);
            } else {
                appendMessage(`Error analyzing file: ${data.error}`, true);
            }
        } catch(e) {
            uploadingSpinner.classList.add('d-none');
            dropText.classList.remove('d-none');
            appendMessage(`Network error during upload.`, true);
        }
        resumeInput.value = ''; // Reset
    }
});
