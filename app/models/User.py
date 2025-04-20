from typing import Optional
from sqlalchemy import  String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, info={'label': 'ID'})
    phone: Mapped[str] = mapped_column(info={'label': 'Телефон'})

    subscriber_mts: Mapped[bool] = mapped_column(info={'label': 'Абонент МТС'})
    tariff: Mapped[str] = mapped_column(info={'label': 'Тариф'})
    mobile_network: Mapped[bool] = mapped_column(info={'label': 'Мобильная связь'})
    home_internet: Mapped[bool] = mapped_column(info={'label': 'Домашний интернет'})
    home_tv: Mapped[bool] = mapped_column(info={'label': 'Домашнее ТВ'})
    home_phone: Mapped[bool] = mapped_column(info={'label': 'Домашний телефон'})
    device: Mapped[str] = mapped_column(info={'label': 'Устройство'})
    os: Mapped[str] = mapped_column(info={'label': 'ОС'})

    my_mts_app_user: Mapped[bool] = mapped_column(info={'label': 'Пользователь приложения Мой МТС'})
    personal_cabinet_user: Mapped[bool] = mapped_column(info={'label': 'Пользователь Личный кабинет'})
    mts_bank_app_user: Mapped[bool] = mapped_column(info={'label': 'Пользователь приложения МТС Банк'})
    mts_money_app_user: Mapped[bool] = mapped_column(info={'label': 'Пользователь приложения МТС Деньги'})

    subscriptions_services_on_number: Mapped[bool] = mapped_column(info={'label': 'Подписки и сервисы на номере'})
    mts_premium: Mapped[bool] = mapped_column(info={'label': 'МТС Premium'})
    mts_cashback: Mapped[bool] = mapped_column(info={'label': 'МТС Cashback'})
    basic_defender: Mapped[bool] = mapped_column(info={'label': 'Защитник базовый'})
    defender_plus: Mapped[bool] = mapped_column(info={'label': 'Защитник+'})

    separate_subscription_kion: Mapped[bool] = mapped_column(info={'label': 'Отдельная подписка Kion'})
    separate_subscription_music: Mapped[bool] = mapped_column(info={'label': 'Отдельная подписка Музыка'})
    separate_subscription_stroki: Mapped[bool] = mapped_column(info={'label': 'Отдельная подписка Строки'})

    debit_card_mts_bank: Mapped[bool] = mapped_column(info={'label': 'Дебетовая карта МТС Банк'})
    credit_card_mts_bank: Mapped[bool] = mapped_column(info={'label': 'Кредитная карта МТС Банк'})
    debit_card_mts_money: Mapped[bool] = mapped_column(info={'label': 'Дебетовая карта МТС Деньги'})
    credit_card_mts_money: Mapped[bool] = mapped_column(info={'label': 'Кредитная карта МТС Деньги'})
    virtual_card_mts_money: Mapped[bool] = mapped_column(info={'label': 'Виртуальная карта МТС Деньги'})

    def to_human_readable(self) -> dict:
        serialized_data = {}
        for column in self.__table__.columns:
            label = column.info.get('label', column.name)
            value = getattr(self, column.name)
            serialized_data[label] = value
        return serialized_data


__all__ = ['User']