# tochka
Тестовое задание для Точки

Проект разработан с использованием фреймворка django.

Требует наличие установленной PostgreSQL базы с именет tochka и логина tochka с паролем tochka.

## Запуск

```
cd <project dir>
./manage.py migrate
./manage.py runserver
```

## Запуск загрузки данных

```
cd <project dir>
./replicate.sh
```
