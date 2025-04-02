from typing import Dict, List, Optional

import requests

from src.models.models import Employer, Vacancy


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    BASE_URL = "https://api.hh.ru/"

    def __init__(self):
        self.session = requests.Session()

    def get_employers(self, employer_ids: List[int]) -> List[Employer]:
        """Получение информации о работодателях по их ID"""
        employers = []
        for employer_id in employer_ids:
            url = f"{self.BASE_URL}employers/{employer_id}"
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                employer = Employer(
                    id=data["id"],
                    name=data["name"],
                    url=data["alternate_url"],
                    open_vacancies=data["open_vacancies"],
                )
                employers.append(employer)
        return employers

    def get_vacancies_by_employer(self, employer_id: str) -> List[Vacancy]:
        """Получение вакансий работодателя по его ID"""
        url = f"{self.BASE_URL}vacancies"
        params = {
            "employer_id": employer_id,
            "per_page": 100,  # Максимальное количество вакансий на странице
            "area": 113,  # Россия
        }
        response = self.session.get(url, params=params)
        vacancies = []
        if response.status_code == 200:
            data = response.json()
            for item in data["items"]:
                salary = self._parse_salary(item.get("salary"))
                vacancy = Vacancy(
                    id=item["id"],
                    employer_id=employer_id,
                    title=item["name"],
                    salary_from=salary["from"],
                    salary_to=salary["to"],
                    currency=salary["currency"],
                    url=item["alternate_url"],
                )
                vacancies.append(vacancy)
        return vacancies

    @staticmethod
    def _parse_salary(salary: Optional[Dict]) -> Dict:
        """Парсинг информации о зарплате"""
        if not salary:
            return {"from": None, "to": None, "currency": None}
        return {
            "from": salary.get("from"),
            "to": salary.get("to"),
            "currency": salary.get("currency"),
        }