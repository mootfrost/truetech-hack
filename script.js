const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');

chatForm.addEventListener('submit', async (e) => {
e.preventDefault();

const message = userInput.value.trim();
if (!message) return;

appendMessage('Вы', message, 'user');
userInput.value = '';

appendMessage('AI', '...', 'bot');

try {
const response = await fetch('https://api.openai.com/v1/chat/completions', {
method: 'POST',
headers: {
'Content-Type': 'application/json',
'Authorization': 'Bearer YOUR_OPENAI_API_KEY'
},
body: JSON.stringify({
model: 'gpt-3.5-turbo',
messages: [
{ role: 'system', content: 'Ты — дружелюбный помощник.' },
{ role: 'user', content: message }
]
})
}); 

updateLastBotMessage(botMessage);
} catch (error) {
updateLastBotMessage('Произошла ошибка при обращении к API.');
console.error('Ошибка:', error);
}
});

const data = await response.json();
const botMessage = data.choices[0].message.content.trim();

updateLastBotMessage(botMessage);

function appendMessage(sender, text, className) {
const messageElem = document.createElement('div');
messageElem.className = 'message ' + className;
messageElem.innerHTML = <span class="${className}">${sender}:</span> + {text};
chatBox.appendChild(messageElem);
chatBox.scrollTop = chatBox.scrollHeight;
}

function updateLastBotMessage(newText) {
const messages = document.querySelectorAll('.message.bot');
const last = messages[messages.length - 1];
if (last) last.innerHTML = <span class="bot">AI:</span> + {newText};
}