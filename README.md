# Онлайн платформа-торговой сети электроники

### Запуск

###### Для запуска локально:

1. Заполните файл ".env.sample" и переименуйте его в ".env"
2. Установить зависимости: `pip install -r requirements.txt`
3. Поднять сайт: `python manage.py runserver`

### Команды

* Заполнить БД: `python manage.py fill_db`
* Создать пользователя: `python manage.py create_user`
* Создать суперпользователя: `python manage.py create_admin`

### Тестирование

* Проверка на соответствие PEP8: `flake8 . --exclude=.venv,env,pyproject.tml,poetry.lock,migrations --ignore=E501`
* Запустить тесты: `coverage run --source=. manage.py test`

##### Команда проекта
* Бобров Александр Андреевич

<hr>

###### DevLog

v0.3
1. Установлены библиотеки drf_yasg, coverage, django-cors-headers
2. Настроено подключение к документации через swagger
3. Добавлены тесты на CRUD для Network
4. Настроен corsheaders

v0.2
1. Для NetworkSerializer запретил изменять задолженность, добавил вывод Contact в Json
2. Для NetworkAdmin добавлен action на обнуление задолженности, ссылка на поставщика, фильтр по названию города
3. Для NetworkListAPIView добавлен фильтр по стране

v0.1
1. Добавлены модели Contact, Network, Product
2. Отображение моделей User, Contact, Network, Product в админке
3. Сериализаторы для моделей User, Contact, Network, Product 
4. Установлена библиотека djangorestframework-simplejwt
5. Добавлен контроллер для регистрации
6. Добавлен CRUD для Network

_v0_
1. Установлены библиотеки Django, psycopg2, python-dotenv, flake8, djangorestframework
2. Все чувствительные данные засекречены
3. Добавлена модель User