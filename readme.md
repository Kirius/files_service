# Files service

## Installation in Ubuntu:

### MySql:
sudo apt-get install mysql-server mysql-client libmysqlclient-dev

configure encoding: http://help.ubuntu.ru/wiki/mysql

CREATE DATABASE files CHARACTER SET utf8;

### Setup environment:
git clone git@github.com:Kirius/files_service.git

mkvirtualenv files

cd file_service

pip install -r requirements.txt

mkdir storage

### Do migrations:
./manage.py migrate

### Run server:
./manage.py runserver



