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
1.Публиковать рецепты
2.Подписываться на публикации других пользователей
3.Добавлять понравившиеся рецепты на свою страницу 'избранное'
4.Создавать 'список покупок' из ингридиентов рецепта для покупки в магазине


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

- 
