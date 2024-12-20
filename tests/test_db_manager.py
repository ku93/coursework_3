import unittest
import configparser
import os
import logging
from src.db_manager import DBManager

# Настройка логирования
logging.basicConfig(level=logging.INFO)


class TestDBManager(unittest.TestCase):
    def setUp(self):
        # Создаем тестовый конфигурационный файл
        self.config_filename = "test_database.ini"
        config = configparser.ConfigParser()
        config["postgresql"] = {
            "host": "localhost",
            "dbname": "test_db",
            "user": "test_user",
            "password": "test_password",
            "port": "5432",
        }
        with open(self.config_filename, "w", encoding="utf-8") as f:
            config.write(f)

        # Инициализируем DBManager
        self.db_manager = DBManager(self.config_filename)
        self.db_manager.create_tables()

    def test_insert_company(self):
        company = {"id": 1, "name": "Test Company"}
        self.db_manager.insert_company(company)
        companies = self.db_manager.get_companies_and_vacancies_count()
        self.assertEqual(len(companies), 1)
        self.assertEqual(companies[0][1], "Test Company")

    def test_insert_vacancy(self):
        company = {"id": 2, "name": "Another Company"}
        self.db_manager.insert_company(company)

        vacancy = {"company_id": 2, "vacancy_title": "Test Vacancy", "salary": 1000, "url": "http://example.com"}
        self.db_manager.insert_vacancy(vacancy)
        vacancies = self.db_manager.get_all_vacancies()
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0][1], "Test Vacancy")

    def test_get_avg_salary(self):
        company = {"id": 3, "name": "Third Company"}
        self.db_manager.insert_company(company)

        vacancy1 = {"company_id": 3, "vacancy_title": "Vacancy 1", "salary": 1500, "url": "http://example.com/1"}
        vacancy2 = {"company_id": 3, "vacancy_title": "Vacancy 2", "salary": 2500, "url": "http://example.com/2"}
        self.db_manager.insert_vacancy(vacancy1)
        self.db_manager.insert_vacancy(vacancy2)

        avg_salary = self.db_manager.get_avg_salary()
        self.assertEqual(avg_salary, 2000)

    def test_get_vacancies_with_keyword(self):
        company = {"id": 4, "name": "Fourth Company"}
        self.db_manager.insert_company(company)

        vacancy = {
            "company_id": 4,
            "vacancy_title": "Keyword Vacancy",
            "salary": 1200,
            "url": "http://example.com/keyword",
        }
        self.db_manager.insert_vacancy(vacancy)

        vacancies = self.db_manager.get_vacancies_with_keyword("Keyword")
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0][1], "Keyword Vacancy")

    def tearDown(self):
        self.db_manager.close()
        if os.path.exists(self.config_filename):
            os.remove(self.config_filename)  # Удаляем тестовый конфигурационный файл
        logging.info("Тестовая база данных и конфигурационный файл удалены.")


if __name__ == "__main__":
    unittest.main()
