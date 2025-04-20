const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const phoneInput = document.getElementById('phone-input');
const idInput = document.getElementById('id-input');
const resultBox = document.getElementById('result-box');
const historyBox = document.getElementById('history-box');
const testModeCheckbox = document.getElementById('test-mode');

chatForm.addEventListener('submit', async (e) => {
e.preventDefault();

const message = userInput.value.trim();
const phone = phoneInput?.value.trim() || '';
const id = idInput?.value.trim() || '';
const testMode = testModeCheckbox.checked;

if (!message) {
alert('Введите запрос');
return;
}


updateResult('⏳ Получение ответа...');

if (testMode) {
const testResponse = {
intent: "Узнать статус заказа",
emotion: 45,
suggesion: [
"Проверить состояние заказа на сайте",
"Позвонить по номеру поддержки 8-800-123-45-67"
]
};
setTimeout(() => {
    renderResult(testResponse);
    appendToHistory(message, testResponse.suggesion?.[0]); // ✅ после получения данных
    }, 500);
    return;
    }

try {
const response = await fetch("http://localhost:3000/op/recommend", {
method: 'POST',
headers: {
'Content-Type': 'application/json'
},
body: JSON.stringify({
question: message,
user_data: {
phone,
id
}
})
});
if (!response.ok) {
    updateResult(`❌ Ошибка ${response.status}: ${response.statusText}`);
    return;
  }
  
  const responseData = await response.json();
  renderResult(responseData);
  appendToHistory(message, responseData.suggesion?.[0]); // ⬅️ добавлено
} catch (error) {
    console.error('Ошибка:', error);
    updateResult('❌ Ошибка соединения с сервером.');
    }
    });
    // Функция для форматирования и отображения результатов
    function renderResult({ intent, emotion, suggesion }) {
    let emotionText = '';
    if (emotion <= 30) emotionText = 'спокоен 😌';
    else if (emotion <= 60) emotionText = 'раздражён 😠';
    else emotionText = 'злой 😡';
    
    const suggestionList = suggesion?.map((s, i) => `🔹 ${s}`).join('<br>') || '—';
    
    const html = `<p><strong>Намерение:</strong> ${intent || 'Не определено'}</p>     <p><strong>Эмоция:</strong> ${emotion} (${emotionText})</p>     <p><strong>Рекомендуем:</strong><br>${suggestionList}</p>`;
    
    resultBox.innerHTML = html;
    }
    
    // Добавление записи в историю
    function appendToHistory(userMessage, firstSuggestion = null) {
        const card = document.createElement('div');
        card.className = 'history-card';
        
        const time = new Date().toLocaleTimeString();
        
        const suggestionHTML = firstSuggestion
        ? `<div class="suggestion">💡 ${firstSuggestion}</div>`
        : '';
        
        card.innerHTML =    ` <div class="history-time">${time}</div>     <div class="history-query">${userMessage}</div>     ${suggestionHTML}  `;
        
        historyBox.prepend(card);
        }
    
    // Обновление результата текстом
    function updateResult(text) {
    resultBox.innerHTML = `<p>${text}</p>`;
    }