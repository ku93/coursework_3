import unittest
from unittest.mock import patch, Mock
from src.api import HHAPI


class TestHHAPI(unittest.TestCase):

    def setUp(self):
        self.hh_api = HHAPI()

    @patch("requests.get")
    def test_get_companies_success(self, mock_get):
        # Мокируем ответ API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "1740", "name": "Test Company"}
        mock_get.return_value = mock_response

        company_ids = ["1740"]
        companies = self.hh_api.get_companies(company_ids)

        self.assertEqual(len(companies), 1)
        self.assertEqual(companies[0]["id"], "1740")
        self.assertEqual(companies[0]["name"], "Test Company")

    @patch("requests.get")
    def test_get_companies_failure(self, mock_get):
        # Мокируем ответ API с ошибкой
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        company_ids = ["9999"]  # Не существующий ID
        companies = self.hh_api.get_companies(company_ids)

        self.assertEqual(len(companies), 0)

    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        # Мокируем ответ API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Software Engineer",
                    "employer": {"name": "Test Company"},
                    "salary": {"from": 1000},
                    "alternate_url": "http://example.com/vacancy",
                }
            ]
        }
        mock_get.return_value = mock_response

        employer_id = "1740"
        vacancies = self.hh_api.get_vacancies(employer_id)

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]["vacancy_title"], "Software Engineer")
        self.assertEqual(vacancies[0]["company_name"], "Test Company")
        self.assertEqual(vacancies[0]["salary"], 1000)
        self.assertEqual(vacancies[0]["url"], "http://example.com/vacancy")

    @patch("requests.get")
    def test_get_all_vacancies(self, mock_get):
        # Мокируем ответ API для двух компаний
        mock_response_1 = Mock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = {
            "items": [
                {
                    "name": "Software Engineer",
                    "employer": {"name": "Company A"},
                    "salary": {"from": 1000},
                    "alternate_url": "http://example.com/vacancy_a",
                }
            ]
        }
        mock_response_2 = Mock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = {
            "items": [
                {
                    "name": "Data Scientist",
                    "employer": {"name": "Company B"},
                    "salary": {"from": 1200},
                    "alternate_url": "http://example.com/vacancy_b",
                }
            ]
        }
        mock_get.side_effect = [mock_response_1, mock_response_2]

        company_ids = ["1740", "3529"]
        all_vacancies = self.hh_api.get_all_vacancies(company_ids)

        self.assertEqual(len(all_vacancies), 2)
        self.assertEqual(all_vacancies[0]["vacancy_title"], "Software Engineer")
        self.assertEqual(all_vacancies[1]["vacancy_title"], "Data Scientist")


if __name__ == "__main__":
    unittest.main()
