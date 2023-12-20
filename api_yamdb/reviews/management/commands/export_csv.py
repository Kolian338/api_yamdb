import csv
import glob
import os

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist


DictFileModel = {
    'category.csv': 'Categories',
    'comments.csv': 'Comment',
    'genre_title.csv': 'GenreTitles',
    'genre.csv': 'Genre',
    'review.csv': 'Review',
    'titles.csv': 'Title',
    'users.csv': 'User'
}


def LoadRow(reader,
            model,
            subo_model,
            fields_name):
    for row in reader:
        try:
            object_model = model()
            for i, field in enumerate(row):
                if subo_model.get(i):
                    # field значение поля, например 1
                    # # subo_model имя поля, например title
                    #print(f'object_model {object_model}')
                    #print(f'object_model2 {object_model._meta.get_field(subo_model.get(i))}')
                    #print(f'object_model3 {object_model._meta.get_field(subo_model.get(i)).related_model}')
                    #print(f'Зашли в subo_model {subo_model[i]}')
                    try:
                        obj_subo_model = (object_model.
                                          _meta.get_field(subo_model.get(i)).
                                          related_model)
                        #obj_subo_model2 = object_model._meta.get_field(subo_model.get(i))
                        #obj_subo_model3 = obj_subo_model2.related_model.objects.all()
                        #obj_subo_model4 = obj_subo_model2.related_model.objects.filter(id=field)
                        #obj_subo_model5 = obj_subo_model2.related_model.objects.get(pk=field)
                        # obj_subo_model = apps.get_model('reviews',subo_model[i])()
                        print(f'Поле которое хотим получитьь {field}')
                        #print(f'Объект subo_model {obj_subo_model}')
                        print(f'Откуда хотим получить {obj_subo_model}')
                        try:
                            obj = obj_subo_model.objects.get(id=field)
                            print(f'Что получили {obj}')
                        except ObjectDoesNotExist:
                            raise (f'Не удалось получить '
                                   f'объект {obj} с id {field}')
                        #print(f'Объект subo_model4 {obj_subo_model4}')
                        #print(f'Объект subo_model5 {obj_subo_model5}')
                        #field = obj_subo_model3.objects.get(pk=field)
                        #obj_subo_model5 = obj_subo_model2.related_model.objects.get(pk=field)
                        #field = obj_subo_model3.filter(pk=field)
                        #print(f'Поле subo_model {field}')
                    except ObjectDoesNotExist:
                        raise (f'Не удалось получить '
                               f'объект {obj_subo_model} с id {field}')
                    setattr(object_model, fields_name[i], field)
                    print(f'Откуда хотим получить {obj_subo_model}')
            object_model.save()
        except Exception as err:
            print(err)
        print(f'subo_model {subo_model}') 


def CheckField(reader, model_fields, model_name):
    print(f'Проверка полей модели {model_name}')
    fields_name = reader.__next__()
    subo_model = {}
    for i, field in enumerate(fields_name):
        if field.endswith('_id'):
            fields_name[i] = field.replace('_id', '')
            subo_model[i] = fields_name[i]
            print(f'Добавили подчиненную модель {subo_model[i]}')
        if fields_name[i] not in model_fields:
            raise CommandError(f'В модели {model_name}'
                               f' нет поля {field}!')
    return subo_model, fields_name


class Command(BaseCommand):
    """Команда для загрузки данных в БД из csv файла"""
    help = 'Загрузка csv из указанного каталога.'
    'Пример команды python manage.py export_csv /home/dev/catalog_csv'

    def add_arguments(self, parser):
        parser.add_argument('catalog', type=str)

    def handle(self, *args, **options):
        files = [f for f in glob.glob(options['catalog'] + '/*.csv',
                                      recursive=True)]
        for file in files:
            filename = os.path.basename(file)
            print(f'Загружаем файл {filename}')
            try:
                model_name = DictFileModel.get(filename,
                                               f'Файл {filename} не известен')
                model = apps.get_model('reviews', model_name)
                model_fields = [field.name for field in model._meta.fields]
                with open(file, 'r') as file:
                    reader = csv.reader(file)
                    subo_model, fields_name = CheckField(reader,
                                                         model_fields,
                                                         model_name)
                    LoadRow(reader,
                            model,
                            subo_model,
                            fields_name)
            except OSError as err:
                raise (err)
            except Exception as err:
                raise (err)
