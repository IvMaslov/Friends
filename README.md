# Friends
## Description
Простой сервис друзей. Позволяет добавлять в список друзей других пользователей.
## Run
для запуска сервиса, клонируйте его с github
```sh
git clone https://github.com/IvMaslov/Friends.git
```
затем установите зависимости из файла requirements.txt
```sh
pip install -r requirements.txt
```
далее запустите миграции
```sh
python3 manage.py migrate
```
все готово, можно запускать сервис
```sh
python3 manage.py runserver
```
## Docker
Для запуска приложения в docker, необходимо клонировать его с github, затем сделать миграции, далее все готово и можно запускать контейнер
```sh
docker build . -t friends-to-docker --network=host --rm
```
