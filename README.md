# Онлайн платформа-торговой сети электроники

### Запуск

###### Для запуска локально:

1. Заполните файл ".env.sample" и переименуйте его в ".env"
2. Установить зависимости: pip install -r requirements.txt
3. Поднять сайт: python manage.py runserver

##### Команда проекта
* Бобров Александр Андреевич

<hr>

###### DevLog

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