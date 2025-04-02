from config.config import DB_NAME, EMPLOYER_IDS
from src.api.hh_api import HeadHunterAPI
from src.database.db_creator import DBCreator
from src.database.db_manager import DBManager


def main():
    # Создание базы данных и таблиц
    db_creator = DBCreator()
    try:
        db_creator.create_database()
        print(f"База данных {DB_NAME} успешно создана")
    except Exception as e:
        print(f"Ошибка при создании БД: {e}")

    try:
        db_creator.create_tables()
        print("Таблицы успешно созданы")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")

    # Получение данных с hh.ru
    hh_api = HeadHunterAPI()
    db_manager = DBManager(DB_NAME)

    print("\nПолучение данных о работодателях...")
    employers = hh_api.get_employers(EMPLOYER_IDS)
    db_manager.insert_employers([emp.__dict__ for emp in employers])
    print(f"Данные о {len(employers)} работодателях добавлены в БД")

    print("\nПолучение данных о вакансиях...")
    for employer in employers:
        vacancies = hh_api.get_vacancies_by_employer(employer.id)
        db_manager.insert_vacancies([vac.__dict__ for vac in vacancies])
        print(f"Добавлено {len(vacancies)} вакансий для {employer.name}")

    # Взаимодействие с пользователем
    while True:
        print("\nВыберите действие:")
        print("1 - Список компаний и количество вакансий")
        print("2 - Список всех вакансий")
        print("3 - Средняя зарплата по вакансиям")
        print("4 - Вакансии с зарплатой выше средней")
        print("5 - Поиск вакансий по ключевому слову")
        print("0 - Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            companies = db_manager.get_companies_and_vacancies_count()
            print("\nКомпании и количество вакансий:")
            for company in companies:
                print(f"{company['name']}: {company['vacancies_count']}")

        elif choice == "2":
            vacancies = db_manager.get_all_vacancies()
            print("\nВсе вакансии:")
            for vac in vacancies:
                salary = ""
                if vac["salary_from"] or vac["salary_to"]:
                    salary = f" ({vac['salary_from'] or '?'}-{vac['salary_to'] or '?'} {vac['currency'] or ''})"
                print(f"{vac['company']}: {vac['title']}{salary} - {vac['url']}")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print("\nСредняя зарплата:")
            print(f"От: {avg_salary['avg_from']:.2f} {avg_salary['currency']}")
            print(f"До: {avg_salary['avg_to']:.2f} {avg_salary['currency']}")

        elif choice == "4":
            vacancies = db_manager.get_vacancies_with_higher_salary()
            print("\nВакансии с зарплатой выше средней:")
            for vac in vacancies:
                salary = f" ({vac['salary_from'] or '?'}-{vac['salary_to'] or '?'} {vac['currency'] or ''})"
                print(f"{vac['company']}: {vac['title']}{salary} - {vac['url']}")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print(f"\nРезультаты поиска по '{keyword}':")
            for vac in vacancies:
                salary = f" ({vac['salary_from'] or '?'}-{vac['salary_to'] or '?'} {vac['currency'] or ''})"
                print(f"{vac['company']}: {vac['title']}{salary} - {vac['url']}")

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный ввод, попробуйте еще раз")


if __name__ == "__main__":
    main()