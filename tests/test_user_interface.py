import unittest
from unittest.mock import MagicMock
from src.user_interface import (
    display_companies_and_vacancies_count,
    display_all_vacancies,
    display_avg_salary,
    display_vacancies_with_higher_salary,
    display_vacancies_with_keyword,
)


class TestDisplayFunctions(unittest.TestCase):

    def setUp(self):
        self.db_manager = MagicMock()

    def test_display_companies_and_vacancies_count(self):
        self.db_manager.get_companies_and_vacancies_count.return_value = [(1, "Company A", 5), (2, "Company B", 3)]

        with self.assertLogs("src.user_interface", level="INFO") as log:
            display_companies_and_vacancies_count(self.db_manager)

        self.assertIn("Получение количества вакансий у компаний.", log.output)
        self.assertIn("Компания: Company A, Вакансий: 5", log.output)
        self.assertIn("Компания: Company B, Вакансий: 3", log.output)

    def test_display_all_vacancies(self):
        self.db_manager.get_all_vacancies.return_value = [
            ("Company A", "Vacancy A", 1000, "http://example.com/a"),
            ("Company B", "Vacancy B", 2000, "http://example.com/b"),
        ]

        with self.assertLogs("src.user_interface", level="INFO") as log:
            display_all_vacancies(self.db_manager)

        self.assertIn("Получение всех вакансий.", log.output)
        self.assertIn(
            "Компания: Company A, Вакансия: Vacancy A, Зарплата: 1000, Ссылка: http://example.com/a", log.output
        )
        self.assertIn(
            "Компания: Company B, Вакансия: Vacancy B, Зарплата: 2000, Ссылка: http://example.com/b", log.output
        )

    def test_display_avg_salary(self):
        self.db_manager.get_avg_salary.return_value = 1500

        with self.assertLogs("src.user_interface", level="INFO") as log:
            display_avg_salary(self.db_manager)

        self.assertIn("Получение средней зарплаты.", log.output)
        self.assertIn("Средняя зарплата: 1500", log.output)

    def test_display_vacancies_with_higher_salary(self):
        self.db_manager.get_vacancies_with_higher_salary.return_value = [
            ("Company A", "Vacancy A", 2000, "http://example.com/a")
        ]

        with self.assertLogs("src.user_interface", level="INFO") as log:
            display_vacancies_with_higher_salary(self.db_manager)

        self.assertIn("Получение вакансий с зарплатой выше средней.", log.output)
        self.assertIn(
            "Вакансия с зарплатой выше средней: ('Company A', 'Vacancy A', 2000, 'http://example.com/a')", log.output
        )

    def test_display_vacancies_with_keyword(self):
        keyword = "developer"
        self.db_manager.get_vacancies_with_keyword.return_value = [
            ("Company A", "Developer", 1000, "http://example.com/a")
        ]

        with self.assertLogs("src.user_interface", level="INFO") as log:
            display_vacancies_with_keyword(self.db_manager, keyword)

        self.assertIn(f"Получение вакансий по ключевому слову: {keyword}.", log.output)
        self.assertIn(
            "Вакансия по ключевому слову 'developer': ('Company A', 'Developer', 1000, 'http://example.com/a')",
            log.output,
        )


if __name__ == "__main__":
    unittest.main()
