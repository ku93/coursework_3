import logging
from src.db_manager import DBManager
from src.data_loader import DataLoader
from src.user_interface import (
    display_companies_and_vacancies_count,
    display_all_vacancies,
    display_avg_salary,
    display_vacancies_with_higher_salary,
    display_vacancies_with_keyword,
)

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    logging.info("Запуск программы.")

    db_manager = DBManager("../database.ini")
    logging.info("Создание таблиц в базе данных.")
    db_manager.create_tables()

    company_ids = ["1740", "3529", "78638", "2748", "781844", "4934", "80", "2987", "58320", "107434"]
    data_loader = DataLoader(db_manager)

    logging.info("Загрузка данных для компаний с ID: %s", company_ids)
    data_loader.load_data(company_ids)

    logging.info("Отображение количества вакансий у компаний.")
    display_companies_and_vacancies_count(db_manager)

    logging.info("Отображение всех вакансий.")
    display_all_vacancies(db_manager)

    logging.info("Отображение средней зарплаты.")
    display_avg_salary(db_manager)

    logging.info("Отображение вакансий с зарплатой выше средней.")
    display_vacancies_with_higher_salary(db_manager)

    keyword = input("Введите ключевое слово для поиска вакансий: ")
    logging.info("Поиск вакансий по ключевому слову: %s", keyword)
    display_vacancies_with_keyword(db_manager, keyword)

    logging.info("Закрытие соединения с базой данных.")
    db_manager.close()


if __name__ == "__main__":
    main()
