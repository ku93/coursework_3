import unittest
from unittest.mock import MagicMock, patch
from src.data_loader import DataLoader  # Предполагается, что ваш класс DataLoader находится в файле data_loader.py
from src.db_manager import DBManager
from src.api import HHAPI


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        # Создаем моки для DBManager и HHAPI
        self.mock_db_manager = MagicMock(spec=DBManager)
        self.mock_api = MagicMock(spec=HHAPI)

        # Создаем экземпляр DataLoader с моками
        self.data_loader = DataLoader(self.mock_db_manager)
        self.data_loader.api = self.mock_api  # Подменяем API на наш мок

    def test_load_data_companies_found(self):
        # Настраиваем мок API для возврата компаний
        self.mock_api.get_companies.return_value = [
            {"id": "1", "name": "Test Company"},
            {"id": "2", "name": "Another Company"},
        ]

        # Настраиваем мок API для возврата вакансий
        self.mock_api.get_vacancies.side_effect = [
            [{"id": "101", "title": "Test Vacancy 1"}, {"id": "102", "title": "Test Vacancy 2"}],
            [],  # Для второй компании нет вакансий
        ]

        company_ids = ["1", "2"]
        self.data_loader.load_data(company_ids)

        # Проверяем, что компании были добавлены
        self.mock_db_manager.insert_company.assert_any_call({"id": "1", "name": "Test Company"})
        self.mock_db_manager.insert_company.assert_any_call({"id": "2", "name": "Another Company"})

        # Проверяем, что вакансии были добавлены для первой компании
        self.mock_db_manager.insert_vacancy.assert_any_call({"id": "101", "title": "Test Vacancy 1"})
        self.mock_db_manager.insert_vacancy.assert_any_call({"id": "102", "title": "Test Vacancy 2"})

        # Проверяем, что вакансии не были добавлены для второй компании
        self.assertEqual(self.mock_db_manager.insert_vacancy.call_count, 2)

    def test_load_data_no_companies(self):
        # Настраиваем мок API для возврата пустого списка компаний
        self.mock_api.get_companies.return_value = []

        company_ids = ["1", "2"]
        with patch("logging.info") as mock_log_info:
            self.data_loader.load_data(company_ids)
            mock_log_info.assert_called_with("Начало загрузки данных о компаниях и вакансиях.")
            self.mock_db_manager.insert_company.assert_not_called()  # Компании не должны быть добавлены

    def test_load_data_exception_handling(self):
        # Настраиваем мок API для возврата компаний
        self.mock_api.get_companies.return_value = [{"id": "1", "name": "Test Company"}]

        # Настраиваем мок DBManager для выбрасывания исключения при добавлении компании
        self.mock_db_manager.insert_company.side_effect = Exception("DB Error")

        with patch("logging.error") as mock_log_error:
            self.data_loader.load_data(["1"])
            mock_log_error.assert_called_with("Ошибка при загрузке данных для компании Test Company: DB Error")


if __name__ == "__main__":
    unittest.main()
