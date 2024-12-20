import logging
from src.api import HHAPI
from src.db_manager import DBManager


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class DataLoader:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager
        self.api = HHAPI()

    def load_data(self, company_ids: list[str]):
        """Загружает данные о компаниях и вакансиях в БД."""
        logging.info("Начало загрузки данных о компаниях и вакансиях.")
        companies = self.api.get_companies(company_ids)

        if not companies:
            logging.warning("Не найдено компаний для загрузки.")
            return

        for company in companies:
            try:
                self.db_manager.insert_company(company)
                logging.info(f"Компания {company['name']} успешно добавлена в БД.")

                vacancies = self.api.get_vacancies(company["id"])
                if not vacancies:
                    logging.warning(f"Нет вакансий для компании {company['name']}.")
                    continue

                for vacancy in vacancies:
                    self.db_manager.insert_vacancy(vacancy)
                    logging.info(f"Вакансия {vacancy['title']} успешно добавлена для компании {company['name']}.")

            except Exception as e:
                logging.error(f"Ошибка при загрузке данных для компании {company['name']}: {e}")


if __name__ == "__main__":
    db_manager = DBManager("../database.ini")
    data_loader = DataLoader(db_manager)
    company_ids = ["1740", "3529", "78638", "2748", "781844", "4934", "80", "2987", "58320", "107434", "40678"]
    data_loader.load_data(company_ids)
    db_manager.close()
