import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# === Агент, который работает с базой знаний ===
class KnowledgeAgent:
    def __init__(self, knowledge_base):
        """
        knowledge_base — список документов, фактов или текстов
        """
        self.knowledge_base = knowledge_base
        self.vectorizer = TfidfVectorizer()
        self.doc_vectors = self.vectorizer.fit_transform(knowledge_base)  # векторизуем базу знаний

    def retrieve(self, query, top_k=1):
        """
        Находит наиболее релевантные документы из базы
        """
        query_vec = self.vectorizer.transform([query])  # векторизуем запрос
        similarities = cosine_similarity(query_vec, self.doc_vectors).flatten()  # считаем косинусную близость
        top_indices = similarities.argsort()[::-1][:top_k]  # берём топ-K документов

        return [(self.knowledge_base[i], similarities[i]) for i in top_indices]

    def generate_response(self, query):
        """
        Формирует ответ на основе найденной информации
        """
        retrieved = self.retrieve(query, top_k=1)
        if retrieved and retrieved[0][1] > 0.1:  # если достаточно релевантно
            doc, score = retrieved[0]
            return f"📚 Нашёл информацию: {doc}"
        else:
            return "❓ К сожалению, я не нашёл подходящей информации."


# === Пример базы знаний ===
knowledge = [
    "Доставка осуществляется с 10:00 до 22:00 без выходных.",
    "Отменить заказ можно в течение 10 минут после оформления.",
    "Мы работаем в Москве и Санкт-Петербурге.",
    "Среднее время доставки — 45 минут.",
]

# === Пример использования ===
if __name__ == "__main__":
    k_agent = KnowledgeAgent(knowledge)

    query = "Сколько длится доставка?"
    answer = k_agent.generate_response(query)
    print(answer)
