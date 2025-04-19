# config.py
import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


@dataclass
class DBConfig:
    """Конфигурация подключения к базе данных"""

    host: str = "localhost"
    user: str = "postgres"
    password: str = os.getenv(
        "DB_PASSWORD", ""
    )  # Пароль только из переменных окружения
    port: str = "5432"
    dbname: str = "hh_vacancies"

    def get_connection_dict(self) -> dict:
        """Возвращает параметры подключения в виде словаря"""
        return {
            "host": self.host,
            "user": self.user,
            "password": self.password,
            "port": self.port,
            "dbname": self.dbname,
        }


# Инициализация конфигурации
db_config = DBConfig()

# Настройки подключения к БД
DB_CONFIG = db_config.get_connection_dict()

# Название базы данных
DB_NAME = db_config.dbname

# ID компаний для сбора данных
EMPLOYER_IDS = [
    "1740",  # Яндекс
    "3529",  # Сбер
    "78638",  # Тинькофф
    "2748",  # Ростелеком
    "3776",  # МТС
    "41862",  # VK
    "87021",  # Wildberries
    "4934",  # Билайн
    "1122462",  # СберТех
    "1057",  # Касперский
    "2180",  # Ozon
    "3127",  # МегаФон
]
