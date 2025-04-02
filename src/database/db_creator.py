import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config.config import DB_CONFIG


class DBCreator:
    """Класс для создания базы данных и таблиц"""

    def __init__(self):
        self.conn_params = DB_CONFIG.copy()
        self.db_name = self.conn_params.pop("dbname")

    def create_database(self):
        """Создание базы данных"""
        conn = psycopg2.connect(**self.conn_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.db_name))
            )
        conn.close()

    def create_tables(self):
        """Создание таблиц в базе данных"""
        conn = psycopg2.connect(dbname=self.db_name, **self.conn_params)

        with conn.cursor() as cur:
            # Таблица работодателей
            cur.execute(
                """
                CREATE TABLE employers (
                    id VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    url VARCHAR(100),
                    open_vacancies INTEGER
                )
            """
            )

            # Таблица вакансий
            cur.execute(
                """
                CREATE TABLE vacancies (
                    id VARCHAR(20) PRIMARY KEY,
                    employer_id VARCHAR(20) REFERENCES employers(id),
                    title VARCHAR(100) NOT NULL,
                    salary_from NUMERIC(12, 2),
                    salary_to NUMERIC(12, 2),
                    currency VARCHAR(10),
                    url VARCHAR(100)
                )
            """
            )

        conn.commit()
        conn.close()
