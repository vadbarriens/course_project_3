# Проект для сбора и анализа вакансий с сайта hh.ru с сохранением в PostgreSQL

## Содержание

1. Описание проекта
2. Функциональность
3. Технологический стек
4. Установка и настройка
5. Структура проекта
6. Примеры использования
7. База данных
8. Лицензия

## Описание проекта

Проект предназначен для:

- Сбора данных о компаниях и вакансиях с API hh.ru
- Сохранения данных в реляционную БД PostgreSQL
- Анализа рынка вакансий
- Поиска вакансий по различным критериям

## Функциональность

- Получение данных о 10+ компаниях с hh.ru
- Сохранение в PostgreSQL:
    - Информация о компаниях
    - Список вакансий с зарплатами
- Аналитические запросы:
    - Количество вакансий по компаниям
    - Средняя зарплата
    - Вакансии с зарплатой выше средней
    - Поиск по ключевым словам

# Технологический стек

## Основные технологии

- Python 3.9+
- PostgreSQL 13+
- psycopg2 (драйвер PostgreSQL для Python)
-

## Библиотеки Python

- requests - для работы с API hh.ru
- python-dotenv - управление переменными окружения
- psycopg2-binary - взаимодействие с PostgreSQL

# Установка и настройка

## Предварительные требования

1. Установленный Python 3.9+
2. Установленный PostgreSQL 13+
3. Созданная база данных в PostgreSQL

## Шаги установки

1. Клонировать репозиторий:
   git clone https://github.com/vadbarriens/course_project_3

1. Создать и активировать виртуальное окружение: python -m venv venv source venv/bin/activate


2. Установить зависимости: pip install -r requirements.txt

3. оздать файл .env в корне проекта: DB_PASSWORD=your_password_here

4. Запустить приложение: python main.py

## Структура проекта

````
course_project_3/ 
├── config/ # Конфигурация 
│ ├── config.py # Настройки приложения 
├── src/ # Исходный код 
│ ├── api/ # Работа с API 
│ │  ├── hh_api.py # Модуль hh.ru API 
│ ├── database/ # Работа с БД
│ │  ├── db_creator.py # Создание БД
│ │  ├── db_manager.py # Управление БД
│ ├── models/ # Модели данных 
│ │  ├── models.py # Классы Employer и Vacancy
├── .gitignore
├── main.py # Точка входа 
├── README.md 
├── requirements.txt # Зависимости
````

## Примеры использования

1. Получение списка компаний и количества вакансий from src.database.db_manager import DBManager
   db_manager = DBManager('hh_vacancies') companies = db_manager.get_companies_and_vacancies_count()
   for company in companies: print(f"{company['name']}: {company['vacancies_count']} вакансий")

2. Поиск вакансий по ключевому слову python_vacancies = db_manager.get_vacancies_with_keyword('python') for vac in
   python_vacancies: print(f"{vac['company']}: {vac['title']} - {vac['url']}")

## База данных
Проект использует 2 основные таблицы: Таблица employers Поле Тип Описание id VARCHAR(20) ID компании name VARCHAR(100)
Название компании url VARCHAR(100) Ссылка на компанию open_vacancies INTEGER Количество вакансий Таблица vacancies Поле
Тип Описание id VARCHAR(20) ID вакансии employer_id VARCHAR(20) ID компании (FK) title VARCHAR(100) Название вакансии
salary_from NUMERIC(12,2) Минимальная зарплата salary_to NUMERIC(12,2) Максимальная зарплата currency VARCHAR(10) Валюта
зарплаты url VARCHAR(100) Ссылка на вакансию

# Лицензия
MIT
