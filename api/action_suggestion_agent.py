class ActionSuggestionAgent:
    def __init__(self):
        self.rules = {
            ("support", "anger"): "🔧 Немедленно подключить поддержку — клиент раздражён.",
            ("support", "sadness"): "🤝 Проявите эмпатию и уточните проблему.",
            ("support", "joy"): "😊 Клиент доволен, просто поддержите беседу.",
            ("order_food", "joy"): "✅ Заказ оформлен, можно предложить промокод.",
            ("order_food", "anger"): "⚠️ Извинитесь за неудобства, уточните заказ.",
            ("cancel_order", "anger"): "🚨 Успокойте клиента, помогите с отменой.",
            ("get_info", "sadness"): "🧐 Ответьте спокойно и понятно.",
        }

    def suggest_action(self, intent, emotion):
        return self.rules.get((intent, emotion), "📝 Стандартная обработка запроса.")