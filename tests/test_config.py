import unittest
import os
from configparser import ConfigParser
from unittest.mock import patch, MagicMock
from src.config import config


class TestConfigFunction(unittest.TestCase):

    def setUp(self):

        self.config_filename = "test_database.ini"
        with open(self.config_filename, "w") as f:
            f.write("[postgresql]\n")
            f.write("host=localhost\n")
            f.write("database=test_db\n")
            f.write("user=test_user\n")
            f.write("password=test_password\n")

    def tearDown(self):

        if os.path.exists(self.config_filename):
            os.remove(self.config_filename)

    def test_config_success(self):
        """Тест на успешное чтение конфигурации."""
        expected = {"host": "localhost", "database": "test_db", "user": "test_user", "password": "test_password"}
        result = config(filename=self.config_filename)
        self.assertEqual(result, expected)

    def test_config_section_not_found(self):
        """Тест на случай, если секция не найдена."""
        with self.assertRaises(Exception) as context:
            config(filename=self.config_filename, section="mysql")
        self.assertTrue("Секция mysql не найдена в файле" in str(context.exception))

    def test_config_file_not_found(self):
        """Тест на случай, если файл конфигурации не найден."""
        with self.assertRaises(FileNotFoundError):
            config(filename="non_existent_file.ini")


if __name__ == "__main__":
    unittest.main()
