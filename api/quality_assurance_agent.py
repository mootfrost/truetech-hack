import re

class QualityAssuranceAgent:
    def __init__(self):
        self.required_phrases = [
            "пожалуйста",
            "благодарим за обращение",
            "извините",
            "мы рады помочь",
            "хорошего дня",
        ]

        self.forbidden_phrases = [
            "не знаю",
            "это не ко мне",
            "сами разберитесь",
            "почему вы мне пишете",
            "не обязан",
        ]

    def check_response(self, response_text):
        issues = []

        if not any(phrase in response_text.lower() for phrase in self.required_phrases):
            issues.append("🔔 Ответ не содержит вежливых фраз.")

        for bad in self.forbidden_phrases:
            if re.search(rf'\b{re.escape(bad)}\b', response_text.lower()):
                issues.append(f"🚫 Найдена нежелательная фраза: '{bad}'")

        if len(response_text.strip()) < 10:
            issues.append("⚠️ Ответ слишком короткий — возможно, недостаточно информативен.")

        if not issues:
            return "✅ Ответ соответствует стандартам качества."
        else:
            return "\n".join(issues)