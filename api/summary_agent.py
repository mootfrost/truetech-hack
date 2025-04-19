class SummaryAgent:
    def __init__(self):
        self.dialog_history = []

    def record_turn(self, user_text, intent, emotion):
        self.dialog_history.append({
            "user_text": user_text,
            "intent": intent,
            "emotion": emotion
        })

    def generate_summary(self):
        if not self.dialog_history:
            return "Диалог пуст."

        last_intent = self.dialog_history[-1]["intent"]
        dominant_emotion = self._get_dominant_emotion()

        summary = "📝 Резюме диалога:\n"
        summary += f"- Последнее намерение: {last_intent}\n"
        summary += f"- Преобладающая эмоция: {dominant_emotion}\n"
        summary += f"- Кол-во реплик: {len(self.dialog_history)}\n"

        crm_data = {
            "intent": last_intent,
            "dominant_emotion": dominant_emotion,
            "total_turns": len(self.dialog_history),
        }

        return summary, crm_data

    def _get_dominant_emotion(self):
        emotions = [turn["emotion"] for turn in self.dialog_history]
        if emotions:
            return max(set(emotions), key=emotions.count)
        return "neutral"