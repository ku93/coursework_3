import logging
from src.db_manager import DBManager

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def display_companies_and_vacancies_count(db_manager):
    logging.info("Получение количества вакансий у компаний.")
    companies = db_manager.get_companies_and_vacancies_count()
    for company_id, company_name, vacancies_count in companies:
        logging.info(f"Компания: {company_name}, Вакансий: {vacancies_count}")


def display_all_vacancies(db_manager):
    logging.info("Получение всех вакансий.")
    vacancies = db_manager.get_all_vacancies()
    for company_name, vacancy_name, salary, link in vacancies:
        logging.info(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary}, Ссылка: {link}")


def display_avg_salary(db_manager):
    logging.info("Получение средней зарплаты.")
    avg_salary = db_manager.get_avg_salary()
    logging.info(f"Средняя зарплата: {avg_salary}")


def display_vacancies_with_higher_salary(db_manager):
    logging.info("Получение вакансий с зарплатой выше средней.")
    vacancies = db_manager.get_vacancies_with_higher_salary()
    for vacancy in vacancies:
        logging.info(f"Вакансия с зарплатой выше средней: {vacancy}")


def display_vacancies_with_keyword(db_manager, keyword):
    logging.info(f"Получение вакансий по ключевому слову: {keyword}.")
    vacancies = db_manager.get_vacancies_with_keyword(keyword)
    for vacancy in vacancies:
        logging.info(f"Вакансия по ключевому слову '{keyword}': {vacancy}")


if __name__ == "__main__":
    db_manager = DBManager("../database.ini")

    try:
        display_companies_and_vacancies_count(db_manager)
        display_all_vacancies(db_manager)
        display_avg_salary(db_manager)
        display_vacancies_with_higher_salary(db_manager)
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        display_vacancies_with_keyword(db_manager, keyword)
    finally:
        db_manager.close()
        logging.info("Соединение с базой данных закрыто.")
