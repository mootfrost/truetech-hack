from app.models.Base import Base
from app.models.Client import Client
from app.models.Dialog import Dialog

__all__ = ["Client", "Base", 'Dialog']

"""
POST
http://localhost:3000/op/recommend
{
    "question": "вопрос",
    "user_data": {'phone': '', 'id': ''}
}

return
{
    "intent": "намерение пользователя, что он хочет",
    "emotion": 0..100, // 0..30 - спокоен, 30..60 - раздражен, 60..100 - злой
    "suggesion": "Предлагаемое решение"
}

---------

GET
http://localhost:3000/user - ?phone=... / ?id=...

"""
