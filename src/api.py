import requests
import logging
from typing import List, Dict


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class HHAPI:
    BASE_URL = "https://api.hh.ru"

    def __init__(self):
        pass

    def get_companies(self, company_ids: List[str]) -> List[Dict]:
        """Получает информацию о компаниях по их идентификаторам."""
        companies_data = []
        for company_id in company_ids:
            response = requests.get(f"{self.BASE_URL}/employers/{company_id}")
            if response.status_code == 200:
                company_info = response.json()
                companies_data.append({"id": company_info["id"], "name": company_info["name"]})
                logging.info(f"Получена информация о компании: {company_info['name']} (ID: {company_id})")
            else:
                logging.error(f"Ошибка при получении данных о компании {company_id}: {response.status_code}")
        return companies_data

    def get_vacancies(self, employer_id: str) -> List[Dict]:
        """Получает список вакансий для заданного работодателя."""
        vacancies_data = []
        response = requests.get(f"{self.BASE_URL}/vacancies?employer_id={employer_id}")
        if response.status_code == 200:
            vacancies = response.json().get("items", [])
            for vacancy in vacancies:
                salary_from = vacancy.get("salary", {}).get("from") if vacancy.get("salary") else None
                vacancies_data.append(
                    {
                        "company_id": employer_id,
                        "company_name": vacancy["employer"]["name"],
                        "vacancy_title": vacancy["name"],
                        "salary": salary_from,
                        "url": vacancy["alternate_url"],
                    }
                )
                logging.info(f"Добавлена вакансия: {vacancy['name']} для компании {vacancy['employer']['name']}")
        else:
            logging.error(f"Ошибка при получении вакансий для работодателя {employer_id}: {response.status_code}")
        return vacancies_data

    def get_all_vacancies(self, company_ids: List[str]) -> List[Dict]:
        """Получает все вакансии для списка компаний."""
        all_vacancies = []
        for company_id in company_ids:
            vacancies = self.get_vacancies(company_id)
            all_vacancies.extend(vacancies)
        logging.info(f"Получено всего {len(all_vacancies)} вакансий для компаний.")
        return all_vacancies


if __name__ == "__main__":

    company_ids = ["1740", "3529", "78638", "2748", "781844", "4934", "80", "2987", "58320", "107434", "40678"]
    hh_api = HHAPI()

    # Получаем информацию о компаниях
    companies = hh_api.get_companies(company_ids)

    # Получаем вакансии для этих компаний
    all_vacancies = hh_api.get_all_vacancies(company_ids)

    # Выводим информацию о компаниях и их вакансиях
    print("Компании:")
    for company in companies:
        print(f"ID: {company['id']}, Название: {company['name']}")

    print("\nВакансии:")
    for vacancy in all_vacancies:
        print(
            f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['vacancy_title']}, "
            f"Зарплата: {vacancy['salary']}, Ссылка: {vacancy['url']}"
        )
