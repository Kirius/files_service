# Files service

## Installation in Ubuntu:

### MySql:
sudo apt-get install mysql-server mysql-client libmysqlclient-dev

configure encoding: http://help.ubuntu.ru/wiki/mysql

CREATE DATABASE files CHARACTER SET utf8;

### Setup environment:
clone this repo

mkvirtualenv files

cd file_service

pip install -r requirements.txt

### Do migrations:
./manage.py migrate
