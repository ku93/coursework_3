import os
from configparser import ConfigParser
import logging
from typing import Dict


def config(filename: str = "../database.ini", section: str = "postgresql") -> Dict[str, str]:
    """Читает параметры конфигурации из указанного файла и секции."""

    # Проверка существования файла
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл конфигурации '{filename}' не найден.")

    parser = ConfigParser()
    logging.info(f"Чтение конфигурации из файла: {filename}")

    parser.read(filename)
    db: Dict[str, str] = {}

    # Проверка существования секции
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
            logging.info(f"Загружен параметр: {param[0]} = {param[1]}")
    else:
        logging.error(f"Секция {section} не найдена в файле {filename}.")
        raise Exception(f"Секция {section} не найдена в файле {filename}.")

    return db


if __name__ == "__main__":

    try:
        config_data = config()
        print("Загруженные параметры конфигурации:")
        for key, value in config_data.items():
            print(f"{key}: {value}")
    except Exception as e:
        logging.error(f"Ошибка при загрузке конфигурации: {e}")
