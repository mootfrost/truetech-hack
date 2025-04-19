from Intent_agent import IntentAgent
from knowledge_agent import KnowledgeAgent
from emotion_agent import EmotionAgent
from action_suggestion_agent import ActionSuggestionAgent
from summary_agent import SummaryAgent
from quality_assurance_agent import QualityAssuranceAgent

# === Обучающие данные для намерений ===
texts = [
    "Я хочу заказать пиццу",
    "Где находится мой заказ?",
    "Свяжитесь с поддержкой",
    "Отменить доставку",
    "Мне нужна помощь",
    "Помогите пожалуйста",
    "Сколько ждать доставку?",
    "Где вы работаете?",
]

labels = [
    "order_food",
    "track_order",
    "support",
    "cancel_order",
    "support",
    "support",
    "get_info",
    "get_info"
]

# === База знаний ===
knowledge = [
    "Доставка осуществляется с 10:00 до 22:00 без выходных.",
    "Отменить заказ можно в течение 10 минут после оформления.",
    "Мы работаем в Москве и Санкт-Петербурге.",
    "Среднее время доставки — 45 минут.",
]

# === Обучающие данные для эмоций ===
emotion_texts = [
    "Я в бешенстве от вашей доставки!",
    "Спасибо большое, всё супер!",
    "Мне грустно, что так долго ждать",
    "Я очень доволен",
    "Это худший сервис",
    "Вы молодцы, я доволен",
    "Вы издеваетесь?! Где мой заказ?",
    "Это кошмар, а не доставка!",
    "Ужасный сервис!",
    "Вы вообще работаете?",
    "Меня всё устраивает, спасибо!",
    "Очень приятно, быстро привезли.",
]

emotion_labels = [
    "anger", "joy", "sadness", "joy", "anger", "joy",
    "anger", "anger", "anger", "anger", "joy", "joy"
]

# === Инициализация агентов ===
intent_agent = IntentAgent()
intent_agent.train(texts, labels)

knowledge_agent = KnowledgeAgent(knowledge)

emotion_agent = EmotionAgent()
emotion_agent.train(emotion_texts, emotion_labels)

action_agent = ActionSuggestionAgent()
summary_agent = SummaryAgent()
qa_agent = QualityAssuranceAgent()

# === Основной цикл обработки запросов ===
def chat():
    print("🤖 Бот запущен! Напишите сообщение ('выход' или 'резюме')\n")

    while True:
        user_input = input("Вы: ")

        if user_input.lower() in ("выход", "exit", "quit"):
            print("Бот: До свидания! 👋")
            break

        if user_input.lower() == "резюме":
            summary, crm = summary_agent.generate_summary()
            print(summary)
            continue

        # Эмоции
        emotion, emo_conf = emotion_agent.predict_emotion(user_input)
        print(f"[DEBUG] Эмоция: {emotion}, уверенность: {emo_conf:.2f}")

        # Намерения
        intent, conf, response = intent_agent.predict_intent(user_input)
        print(f"[DEBUG] Намерение: {intent}, уверенность: {conf:.2f}")

        # Запись истории
        summary_agent.record_turn(user_input, intent, emotion)

        # Рекомендация действия
        action = action_agent.suggest_action(intent, emotion)
        print(f"[DEBUG] Рекомендация оператору: {action}")

        # Ответ
        final_reply = ""
        if response:
            final_reply = response
        elif intent == "get_info":
            final_reply = knowledge_agent.generate_response(user_input)
        else:
            final_reply = "Я вас понял, но пока не знаю, что с этим делать."

        print(f"Бот: {final_reply}")

        # Проверка качества
        qa_feedback = qa_agent.check_response(final_reply)
        print(f"[QA] Проверка качества: {qa_feedback}")


if __name__ == "__main__":
    chat()
