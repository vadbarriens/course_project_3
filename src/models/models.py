from dataclasses import dataclass


@dataclass
class Employer:
    """Класс для представления работодателя"""

    id: str
    name: str
    url: str
    open_vacancies: int


@dataclass
class Vacancy:
    """Класс для представления вакансии"""

    id: str
    employer_id: str
    title: str
    salary_from: float = None
    salary_to: float = None
    currency: str = None
    url: str = None
