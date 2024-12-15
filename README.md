# Проект Coursework_2

## Описание:

 Проект Coursework_2 - это курсовая работа 

## Установка:


1. Клонируйте репозиторий:
```chatinput
git clone git@github.com:ku93/coursework_2.git
```

2. Установите зависимости:
```chatinput
pip install -r requirements.txt
```

3. Проверьте домашнее задание.

## Функционал:

### Модуль main
Основная функция проекта

### Модуль API

Имеет абстрактный класс AbstractAPI, который содержит в себе базовый url (base_url).

Также в модуле имеется дочерний класс HHAPI(AbstractAPI), который содержит в себе приватный метод подключения к API hh.ru. (_connect)



### Модуль city
Имеет в себе дочерний класс City, который наследуется от абстрактного класса и имеет в себе приватный метод подключения к API hh.ru. (_connect), метод для получения списка городов (get_cities), метод поиск города в списке городов (search_city), метод получение ID города по его имени (get_city_id)


### Модуль Vacancy

меет в себе дочерний класс City, который наследуется от абстрактного класса и имеет в себе приватный метод подключения к API hh.ru. (_connect), метод для получения топ N вакансий по зарплате (top_vacancies), метод для поиска вакансий по заголовку, компании и местоположению (search_vacancies)

### Модуль save_to_file

Имеет в себе абстрактный класс для работы с файлами, который содержит в себе такие абстактные методы как получение данных из файла (read_data), добавление данных в файл (add_data), а также удаление данных из файла по идентификатору (delete_data).
Также модуль содержит дочерний клас JsonFileHandler (класс для работы с JSON-файлами)

Функция main_page генерирует JSON-ответ для главной страницы с данными о транзакциях,
    курсах валют и ценах акций

## Тестирование

Для запуска тестов используйте: pytest

## Автор:
Ткачев Леонид Андреевич [e-mail] (tkachev1993adg@yandex.ru)

## Версия
от 18.11.2024 г.