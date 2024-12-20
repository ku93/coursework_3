import unittest
from unittest.mock import patch, MagicMock
from src.main import main


class TestMain(unittest.TestCase):

    @patch("src.main.DataLoader")
    @patch("src.main.DBManager")
    @patch("src.main.UserInterface")
    @patch("src.main.config")
    @patch("src.main.create_connection")
    def test_main_function(
        self, mock_create_connection, mock_config, mock_UserInterface, mock_DBManager, mock_DataLoader
    ) -> None:
        """Тестирует основную функцию приложения."""

        # Настройка мока для конфигурации
        mock_config.return_value = {
            "host": "localhost",
            "database": "test_db",
            "user": "test_user",
            "password": "test_password",
        }

        # Настройка мока для DBManager
        mock_db_manager = MagicMock()
        mock_DBManager.return_value = mock_db_manager

        # Настройка мока для DataLoader
        mock_data_loader = MagicMock()
        mock_DataLoader.return_value = mock_data_loader

        # Настройка мока для UserInterface
        mock_user_interface = MagicMock()
        mock_UserInterface.return_value = mock_user_interface

        # Запуск основной функции
        with patch("builtins.input", return_value="developer"):  # Мок ввода пользователя
            main()

        # Проверка вызовов
        mock_DBManager.assert_called_once()
        mock_DataLoader.assert_called_once_with(mock_db_manager)
        mock_data_loader.load_companies.assert_called_once()
        mock_data_loader.load_vacancies.assert_called_once()
        mock_UserInterface.assert_called_once_with(mock_db_manager)
        mock_user_interface.display_companies_and_vacancies_count.assert_called_once()
        mock_user_interface.display_all_vacancies.assert_called_once()
        mock_user_interface.display_avg_salary.assert_called_once()
        mock_user_interface.display_high_salary_vacancies.assert_called_once()
        mock_user_interface.display_keyword_vacancies.assert_called_once_with("developer")


if __name__ == "__main__":
    unittest.main()
