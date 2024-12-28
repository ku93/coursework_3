import psycopg2
import configparser
import logging
from typing import List, Dict, Optional


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class DBManager:
    def __init__(self, config_file: str):

        config = configparser.ConfigParser()
        config.read(config_file)

        db_name = config["postgresql"]["dbname"]
        user = config["postgresql"]["user"]
        password = config["postgresql"]["password"]
        host = config["postgresql"]["host"]
        port = config["postgresql"]["port"]

        try:
            self.connection = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
            self.cursor = self.connection.cursor()
            logging.info("Соединение с базой данных успешно установлено.")
        except Exception as e:
            logging.error(f"Ошибка при подключении к базе данных: {e}")
            raise

    def create_tables(self):
        """Создает таблицы для компаний и вакансий."""
        create_companies_table = """
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """

        create_vacancies_table = """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            title VARCHAR(255),
            salary NUMERIC,
            url TEXT
        );
        """

        try:
            self.cursor.execute(create_companies_table)
            self.cursor.execute(create_vacancies_table)
            self.connection.commit()
            logging.info("Таблицы успешно созданы.")
        except Exception as e:
            logging.error(f"Ошибка при создании таблиц: {e}")
            self.connection.rollback()

    def insert_company(self, company: Dict):
        """Вставляет новую компанию в таблицу."""
        insert_query = "INSERT INTO companies (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;"
        try:
            self.cursor.execute(insert_query, (company["id"], company["name"]))
            self.connection.commit()
            logging.info(f"Компания {company['name']} успешно добавлена.")
        except Exception as e:
            logging.error(f"Ошибка при вставке компании: {e}")
            self.connection.rollback()

    def insert_vacancy(self, vacancy: Dict):
        """Вставляет новую вакансию в таблицу."""
        insert_query = "INSERT INTO vacancies (company_id, title, salary, url) VALUES (%s, %s, %s, %s);"
        try:
            self.cursor.execute(
                insert_query, (vacancy["company_id"], vacancy["vacancy_title"], vacancy["salary"], vacancy["url"])
            )
            self.connection.commit()
            logging.info(f"Вакансия {vacancy['vacancy_title']} успешно добавлена.")
        except Exception as e:
            logging.error(f"Ошибка при вставке вакансии: {e}")
            self.connection.rollback()

    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        query = """
        SELECT c.id, c.name, COUNT(v.id) AS vacancy_count
        FROM companies c
        LEFT JOIN vacancies v ON c.id = v.company_id
        GROUP BY c.id;
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            logging.info("Данные о компаниях и количестве вакансий успешно получены.")
            return result
        except Exception as e:
            logging.error(f"Ошибка при получении данных о компаниях: {e}")
            return []

    def get_all_vacancies(self) -> List[Dict]:
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        query = """
        SELECT c.name, v.title, v.salary, v.url
        FROM vacancies v
        JOIN companies c ON v.company_id = c.id;
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            logging.info("Данные о всех вакансиях успешно получены.")
            return result
        except Exception as e:
            logging.error(f"Ошибка при получении всех вакансий: {e}")
            return []

    def get_avg_salary(self) -> Optional[float]:
        """Получает среднюю зарплату по вакансиям."""
        query = "SELECT AVG(salary) FROM vacancies;"
        try:
            self.cursor.execute(query)
            avg_salary = self.cursor.fetchone()[0]
            logging.info(f"Средняя зарплата по вакансиям: {avg_salary}")
            return avg_salary
        except Exception as e:
            logging.error(f"Ошибка при получении средней зарплаты: {e}")
            return None

    def get_vacancies_with_higher_salary(self) -> List[Dict]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        query = "SELECT * FROM vacancies WHERE salary > %s;"
        try:
            self.cursor.execute(query, (avg_salary,))
            result = self.cursor.fetchall()
            logging.info(f"Вакансии с зарплатой выше средней успешно получены.")
            return result
        except Exception as e:
            logging.error(f"Ошибка при получении вакансий с зарплатой выше средней: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        query = "SELECT * FROM vacancies WHERE title ILIKE %s;"
        try:
            self.cursor.execute(query, (f"%{keyword}%",))
            result = self.cursor.fetchall()
            logging.info(f"Вакансии с ключевым словом '{keyword}' успешно получены.")
            return result
        except Exception as e:
            logging.error(f"Ошибка при получении вакансий с ключевым словом '{keyword}': {e}")
            return []

    def close(self):
        """Закрывает соединение с БД."""
        self.cursor.close()
        self.connection.close()
        logging.info("Соединение с базой данных закрыто.")


if __name__ == "__main__":
    db_manager = DBManager("../database.ini")
    db_manager.create_tables()
    print(db_manager.get_companies_and_vacancies_count())
    db_manager.close()
