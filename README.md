### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/zinvas/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Описание апи:

Апи предназначен для получения информация 

После запуска проекта будет доступно полное аписание апи

```
http://127.0.0.1:8000/redoc/
```

Сcылка на скачиваение yaml

```
http://127.0.0.1:8000/static/redoc.yaml
```
