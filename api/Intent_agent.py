import re  # для работы с регулярными выражениями (очистка текста)
import nltk  # библиотека для обработки естественного языка
import joblib  # для сохранения и загрузки модели
from nltk.corpus import stopwords  # список "пустых" слов (и, в, на и т.п.)
from sklearn.pipeline import Pipeline  # позволяет объединить шаги обработки в цепочку
from sklearn.feature_extraction.text import TfidfVectorizer  # векторизация текста по TF-IDF
from sklearn.linear_model import LogisticRegression  # классическая модель классификации
from sklearn.ensemble import RandomForestClassifier  # более мощная модель — "лес" деревьев решений

# Загрузка стоп-слов из корпуса NLTK
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('russian'))  # список стоп-слов для русского языка

# === Класс обработчика поддержки ===
class SupportHandler:
    def handle(self, user_text):
        # Метод вызывается, если намерение пользователя — "поддержка"
        return "Понимаю, что вам нужна помощь. Что случилось?"


# === Основной класс агента, который определяет намерения ===
class IntentAgent:
    def __init__(self):
        self.pipeline = None  # сюда загрузим пайплайн с векторизатором и моделью
        self.support_handler = SupportHandler()  # подключаем обработчик поддержки

    def preprocess(self, text):
        """
        Предобработка текста:
        - приведение к нижнему регистру
        - удаление пунктуации
        - удаление стоп-слов
        """
        text = text.lower()  # нижний регистр
        text = re.sub(r'[^\w\s]', '', text)  # удаление пунктуации
        tokens = text.split()  # разбивка на слова
        tokens = [t for t in tokens if t not in STOPWORDS]  # удаление стоп-слов
        return ' '.join(tokens)

    def train(self, texts, labels):
        """
        Обучение модели:
        - предобработка текстов
        - создание пайплайна (векторизация + классификатор)
        - обучение модели
        """
        processed_texts = [self.preprocess(text) for text in texts]

        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),  # превращаем текст в векторы
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))  # обучаем RandomForest
        ])

        self.pipeline.fit(processed_texts, labels)  # обучение модели

    def predict_intent(self, text):
        """
        Предсказание намерения:
        - предобработка
        - получение вероятности и метки
        - активация поддержки при необходимости
        """
        processed = self.preprocess(text)
        intent = self.pipeline.predict([processed])[0]  # определяем метку
        confidence = max(self.pipeline.predict_proba([processed])[0])  # определяем уверенность

        # Если пользователь просит поддержки — активируем SupportHandler
        if intent == "support":
            response = self.support_handler.handle(text)
            return intent, confidence, response

        return intent, confidence, None  # возвращаем намерение, уверенность, и ответ (если есть)

    def save_model(self, path='intent_agent.pkl'):
        """Сохраняем обученный пайплайн в файл"""
        joblib.dump(self.pipeline, path)

    def load_model(self, path='intent_agent.pkl'):
        """Загружаем модель из файла"""
        self.pipeline = joblib.load(path)


# === Пример запуска модели ===
if __name__ == "__main__":
    # Обучающие данные: пары (фраза, метка-намерения)
    texts = [
        "Я хочу заказать пиццу",
        "Где находится мой заказ?",
        "Свяжитесь с поддержкой",
        "Отменить доставку",
        "Мне нужна помощь",
        "Помогите пожалуйста",
    ]

    labels = [
        "order_food",   # заказать еду
        "track_order",  # отслеживание заказа
        "support",      # запрос поддержки
        "cancel_order", # отмена заказа
        "support",      # снова поддержка
        "support"       # и снова
    ]

    # Создаём агента и обучаем
    agent = IntentAgent()
    agent.train(texts, labels)

    # Пример запроса от пользователя
    query = "Мне нужна помощь"
    intent, confidence, response = agent.predict_intent(query)

    # Выводим результат
    print(f"🔍 Намерение: {intent}, уверенность: {confidence:.2f}")
    if response:
        print("🤖 Ответ:", response)
