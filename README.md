# Friends
## Description
Простой сервис друзей. Позволяет добавлять в список друзей других пользователей.
## Run
Для запуска сервиса, клонируйте его с github
```sh
git clone https://github.com/IvMaslov/Friends.git
```
Затем установите зависимости из файла requirements.txt
```sh
pip install -r requirements.txt
```
Далее запустите миграции
```sh
python3 manage.py migrate
```
Все готово, можно запускать сервис
```sh
python3 manage.py runserver
```
## Docker
Для запуска приложения в docker, необходимо клонировать его с github, затем сделать миграции, далее все готово и можно запускать сервис в контейнере
```sh
docker build . -t friends-to-docker --network=host --rm
```
## Usage
Для взаимодействия с API сервиса есть Swagger интерфейс, доступный по ссылке `localhost:8000/swagger`
так же есть OpenAPI спецификация, доступная по ссылке `localhost:8000/redoc`
Существует UI, доступный по ссылке `localhost:8000` который зайдействует все функции API. 

Пример использования UI:
1. Регистрируете пользователя по ссылке `localhost:8000/signup`
2. Регистрируетесь в качестве только что созданного пользователя по ссылке `localhost:8000/login`
3. Пользуетесь сервисом :smiley: