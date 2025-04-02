from typing import Dict, List

import psycopg2

from config.config import DB_CONFIG


class DBManager:
    """Класс для управления базой данных вакансий"""

    def __init__(self, db_name: str):
        self.conn_params = DB_CONFIG.copy()
        self.conn_params["dbname"] = db_name

    def _connect(self):
        """Установка соединения с БД"""
        return psycopg2.connect(**self.conn_params)

    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """
        Получает список всех компаний и количество вакансий у каждой компании

        Returns:
            List[Dict]: Список словарей с информацией о компаниях и количестве вакансий
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, COUNT(v.id) as vacancies_count
                    FROM employers e
                    LEFT JOIN vacancies v ON e.id = v.employer_id
                    GROUP BY e.id
                    ORDER BY vacancies_count DESC
                """
                )
                return [
                    {"name": row[0], "vacancies_count": row[1]}
                    for row in cur.fetchall()
                ]

    def get_all_vacancies(self) -> List[Dict]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию

        Returns:
            List[Dict]: Список словарей с информацией о вакансиях
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, v.title,
                           v.salary_from, v.salary_to, v.currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    ORDER BY e.name, v.title
                """
                )
                return [
                    {
                        "company": row[0],
                        "title": row[1],
                        "salary_from": row[2],
                        "salary_to": row[3],
                        "currency": row[4],
                        "url": row[5],
                    }
                    for row in cur.fetchall()
                ]

    def get_avg_salary(self) -> Dict:
        """
        Получает среднюю зарплату по вакансиям

        Returns:
            Dict: Словарь с информацией о средней зарплате
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        AVG(salary_from) as avg_from,
                        AVG(salary_to) as avg_to,
                        currency
                    FROM vacancies
                    WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
                    GROUP BY currency
                """
                )
                results = cur.fetchall()
                return {
                    "avg_from": results[0][0] if results else None,
                    "avg_to": results[0][1] if results else None,
                    "currency": results[0][2] if results else None,
                }

    def get_vacancies_with_higher_salary(self) -> List[Dict]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям

        Returns:
            List[Dict]: Список вакансий с зарплатой выше средней
        """
        avg_salary = self.get_avg_salary()
        if not avg_salary["avg_from"]:
            return []

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, v.title,
                           v.salary_from, v.salary_to, v.currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    WHERE (v.salary_from > %s OR v.salary_to > %s)
                    ORDER BY e.name, v.title
                """,
                    (avg_salary["avg_from"], avg_salary["avg_from"]),
                )
                return [
                    {
                        "company": row[0],
                        "title": row[1],
                        "salary_from": row[2],
                        "salary_to": row[3],
                        "currency": row[4],
                        "url": row[5],
                    }
                    for row in cur.fetchall()
                ]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные слова

        Args:
            keyword (str): Ключевое слово для поиска в названиях вакансий

        Returns:
            List[Dict]: Список вакансий, содержащих ключевое слово в названии
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, v.title,
                           v.salary_from, v.salary_to, v.currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    WHERE LOWER(v.title) LIKE %s
                    ORDER BY e.name, v.title
                """,
                    (f"%{keyword.lower()}%",),
                )
                return [
                    {
                        "company": row[0],
                        "title": row[1],
                        "salary_from": row[2],
                        "salary_to": row[3],
                        "currency": row[4],
                        "url": row[5],
                    }
                    for row in cur.fetchall()
                ]

    def insert_employers(self, employers: List[Dict]) -> None:
        """Добавление работодателей в БД"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                for employer in employers:
                    cur.execute(
                        """
                        INSERT INTO employers (id, name, url, open_vacancies)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """,
                        (
                            employer["id"],
                            employer["name"],
                            employer["url"],
                            employer["open_vacancies"],
                        ),
                    )
            conn.commit()

    def insert_vacancies(self, vacancies: List[Dict]) -> None:
        """Добавление вакансий в БД"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                for vacancy in vacancies:
                    cur.execute(
                        """
                        INSERT INTO vacancies
                        (id, employer_id, title, salary_from, salary_to, currency, url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """,
                        (
                            vacancy["id"],
                            vacancy["employer_id"],
                            vacancy["title"],
                            vacancy["salary_from"],
                            vacancy["salary_to"],
                            vacancy["currency"],
                            vacancy["url"],
                        ),
                    )
            conn.commit()