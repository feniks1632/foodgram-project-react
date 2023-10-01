# Cервис Foodgram, "Продуктовый помощник"   

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Описание
Сайт на котором пользователи могут:
- Публиковать рецепты
- Подписываться на публикации других пользователей
- Добавлять понравившиеся рецепты на свою страницу 'избранное'
- Создавать 'список покупок' из ингридиентов рецепта для покупки в магазине


### Возможности сайта 
- Аутентификация реализована с помощью модуля DRF - Authtoken.
- У неаутентифицированных пользователей доступ только на уровне чтения.
- Создание объектов разрешено только аутентифицированным пользователям.
- Управление пользователями.
- Возможность подписаться на других пользователей и отписаться от них.
- Получение списка всех тегов и ингредиентов.
- Получение списка всех рецептов.
- Создание рецептов.
- Получение, обновление и удаление конкретного рецепта.
- Возможность добавить рецепт в избранное.
- Возможность добавить рецепт в список покупок.
- Возможность скачать список покупок в txt формате.
- Фильтрация по полям.

#### Используемые технологи
- Python 3.9
- Django 3.2.15
- Django Rest Framework 3.14.0
- Docker
- Docker-compose
- PostgreSQL
- Gunicorn
- Nginx
- GitHub Actions

  ### Для локального запуска проекта вам понадобится:
  - Склонировать репозиторий:

```bash
   git clone <название репозитория>
```

```bash
   cd <название репозитория> 
```

Cоздать и активировать виртуальное окружение:

Команда для установки виртуального окружения:

```bash
   python3 -m venv env
   source env/bin/activate
```

Команда для Windows:

```bash
   python -m venv venv
   source venv/Scripts/activate
```

- Перейти в директорию infra:

```bash
   cd infra
```

- Создать файл .env по образцу(находится в папке infra env.example):

- Документацию можно посмотреть после выполнения команды:
  (Документация находится по адресу http://localhost/api/docs/) 

```bash
   docker-compose up 
```

Установить зависимости из файла requirements.txt:

```bash
   cd ..
   cd backend
   pip install -r requirements.txt
```

```bash
   python manage.py migrate
```

Заполнить базу тестовыми данными об ингредиентах:

```bash
   python manage.py load_ingredients
```

Создать суперпользователя, (если необходимо):

```bash
python manage.py createsuperuser
```

- Запустить локальный сервер:

```bash
   python manage.py runserver
```

### Установка на удалённом сервере

- Выполнить вход на удаленный сервер
- Установить Docker и docker-compose:
- Установка Docker
```bash
   sudo apt install docker.io
   ```

- Установка docker-compose:

``` bash
    sudo apt install docker-compose     
```

или воспользоваться официальной [инструкцией](https://docs.docker.com/compose/install/)

- Находясь локально в директории infra/, скопировать файлы docker-compose.yml и nginx.conf на удаленный сервер:

```bash
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
```
Либо создать docker-compose.yml и nginx.conf ручками(в корне)
```bash
touch docker-compose.yml
touch nginx.conf
```
- Далее Выполните команду:
```bash
sudo docker-compose up -d(флаг -d нужен для запуска контейнеров в фоновом режиме)
```

- Примените миграции:

```bash
   sudo docker-compose exec backend python manage.py migrate
```

- Подгружаем статику:

```bash
   sudo docker-compose exec backend python manage.py collectstatic --no-input
```

- Заполните базу тестовыми данными об ингредиентах:

```bash
   sudo docker-compose exec backend python manage.py load_ingredients
```

- Создайте суперпользователя:

```bash
   sudo docker-compose exec backend python manage.py createsuperuser
```

#### Примеры некоторых запросов API

Регистрация пользователя:

```bash
   POST /api/v1/users/
```

Получение данных своей учетной записи:

```bash
   GET /api/v1/users/me/ 
```

Добавление подписки:

```bash
   POST /api/v1/users/id/subscribe/
```

Обновление рецепта:
  
```bash
   PATCH /api/v1/recipes/id/
```

Удаление рецепта из избранного:

```bash
   DELETE /api/v1/recipes/id/favorite/
```


Проект доступен по адресу: <https://foodgrams1632.ddns.net>

Доступ в админ-панель:

```bash
   логин - hovard
   пароль - qwerty123
```

#### Полный список запросов API находятся в документации

#### Автор проекта

Никита Бражников - (https://github.com/feniks1632)
