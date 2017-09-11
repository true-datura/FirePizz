# FirePizza

Test task for Document

## Getting started:

### Prerequisites

You must install python3, python3-dev and some libs for Pillow.

### Installation

Clone this repo:  
```sh
git clone https://github.com/true-datura/FirePizza
```
Cd in cloned repo directory:  
```sh
cd FirePizza
```  
Create virtualenv, activate it, and install requirements:
```sh
virtualenv -p python3 .env
. .env/bin/activate
pip install -r requirements.txt
```  
Cd in app directory:  
```sh
cd fire_pizza
```
Migrate:
```sh
python manage.py migrate
```  
Create superuser:
```sh
python manage.py createsuperuser
```  
Run dev server:
```sh
python manage.py runserver
```
