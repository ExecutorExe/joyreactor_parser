v0.2.0 ; anaconda3 

# Требования

- python>=3.7

- [requirements.txt](https://github.com/ExecutorExe/joyparser/blob/master/requirements.txt)
# Установка

После активации нужной среды выполните команды
```bash
# get site-packages dir
tmp=$(python3 -c 'import site; print(site.getsitepackages()[0])')/joyparser
# clone package to env package-dir
git clone https://github.com/ExecutorExe/joyparser ${tmp}
```
Если Anaconda
```bash
conda install --file ${tmp}/requirements.txt
```
Если Python
```bash
pip install -r ${tmp}/requirements.txt
```

# Документация
page_max (page): - Определяет максимальное количество страниц

- Принимает страницу

-- возвращает int число
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
parser(page, from_page, until_page=0, update_parsed_array=None)

- page - Первый аргумент это какая страница дожна быть просканирована| "://" обязателен, на конце не должно быть "/"
например http://joyreactor.cc/tag/котэ

- from_page - Второй аргумент получает цифру от какой страницы сканировать


- until_page - Третий аргумент получает цифру до какой страницы сканировать (по умолчанию 0)


- update_parsed_array принимает уже отпарсеный список(images,info,txt) и обновит до первого совпавшего поста(не обязательный аргумент)

    по умолчанию выключен

-- Возвращает

return images, info, txt
    
-- 0 - многомерный список с картинками поста
    
-- 1 - многомерный список с многомерными списками с информацией  [tags,rating, date, keys, lencomments]
    
-- 2 - многомерный список с текстом и лучшими комментами

Пример:

```python
from joyparser import jp
import sys
import os

till_page = 0  # до какой | http://joyreactor.cc/user/котэ/1
#
page = "http://joyreactor.cc/tag/котэ"
# какая пейджа  пример http://joyreactor.cc/котэ (без оканчания на "/")
if sys.platform == "linux" or sys.platform == "win32":
    info_struct.d_path = os.path.join(os.path.expanduser("~"), "Downloads")

from_page = 2
# от какой страницы | например http://joyreactor.cc/user/котэ/2 
# или воспользуйтесь jp.page_max(page) эта функция вернет максимальное количество страниц

img, info, txt = jp.parser(page, from_page, till_page)
jp.download_images(jp.get_rdy(img[jp.sort_by_rate_comments(info[1], 10)]))

```
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
def parse_page(link: str,base:dict,upd=False)
Похоже на parser но сканирует одну страницу и изменяем входной аргумент base (dict)
Каждый ключ словаря == номер поста каждый елемент содержит си подобную структуру

self.images = images

self.text = text

self.tags = tags

self.rating = rating

self.datetime = datetime

self.comments_len = comments_len

upd=True прервет саканирование если найдет любое совпадение
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
filter_by_tag(info=list, tagexceptions=list, spike=None)
     индекс тегов - info[0]


   - info: принемает масив с информацией
   
   - tagexceptions: список с исключениями которые вы выбераете например [хоба!, anime]
   
   - spike: по умолчанию если все теги присудствуют то пост будет считаться
    засчитаным, если же вы поставите 1 то достаточно будет одного тега для того что бы пост прошел
    
   -- возвращает новый отсортированный список индексов

```python
import numpy as np
from joyparser import jp

value = np.array([[1, 2, 3, 4],
                  [11, 22, 33, 44],
                  [111, 222, 333, 444]])
indexes = np.array([10, 5, 7])
print(value[jp.filter_by_tag(value, [1, 2])])
# output [[1 2 3 4]]
print(value[jp.filter_by_tag(value, [1, 2, 44])])
# IndexError: arrays used as indices must be of integer (or boolean) type
# потому что нет результатов от все трех запрашиваемых значений
print(value[jp.filter_by_tag(value, [1, 2, 44], spike=1)])
# output
# [[ 1  2  3  4]
# [11 22 33 44]]
```
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
except_tag(info=list, tagexceptions=list, spike=None)
    
   индекс тегов - info[0]

 - info: принемает масив с информацией
 
 - tagexceptions: список с исключениями которые вы выбераете например [фурри, furry]
 
 - spike: по умолчанию если все теги присудствуют то пост будет считаться
    засчитаным в исключение, если же вы поставите 1 то достаточно будет одного тега для того что бы пост попал в исключение
    
 -- возвращает индексы
 
 Все тоже самое что и sort_by_tag просто исключения тегов
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
filer_by_rate_comments(info_index, rating=0)
    
   Рейтинг = imfo[1] | Комменты - imfo[4]

 - info: 1 аргумент переменная с информацией
 
 - rating: 2 аргумент - цифра, ниже этого значения посты не пройдут
 
 -- отсортированные индексы
 
 Пример:

 ```python
import numpy as np
from joyparser import jp

value = np.array([[1, 2, 3, 4],
                  [11, 22, 33, 44],
                  [111, 222, 333, 444]])
indexes = np.array([10, 5, 7])
print(value[jp.filer_by_rate_comments(indexes, 6)])

# output
# [[  1   2   3   4]
# [111 222 333 444]]
# или можно воспользоваться np.where 

print(value[np.where(indexes >= 6)])

# output
# [[  1   2   3   4]
# [111 222 333 444]]
```
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
get_val_by_index(value, index):
    
   возвращает элементы по индексу

 - value: элементы для сортировки
 
 - index: индексы
 
 -- возвращает значения по индексам
    
Вы также можите отсортировать переменную без этой функции так же как с нумпай массивом

Пример:
```python
import numpy as np

index = np.array([1,2,3])
values = np.array([0,1,2,3])
print(values[index])
# output == [1 2 3]
```
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
get_rdy(images)

Нужна для функции download_images

- Принимает переменную с картинками после парса или после сортировки


-- Возвращает numpy array 1d


-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
download_images(images, multprocess_d = False, warn_on=True)

- 1 аргумент принимает одномерный массив/список изображений

- 2 аргумент включает multiprocess download (выключено по умолчанию)

- 3 аргумент отключения предупреждений по уполчанию влючено True/False
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
votegun(posts_array, cookie, token, vote=True, __abyss="0")

плюсо/минусо-мет
(просьба не злоупотреблять этой функцией)

- posts_array: номера постов(одномерный масив)
  
- token: все тоже самое что и с куки, в самом низу должен быть токен

- vote: голосует за или против(True/False)

- cookie (global info_struct): куки(что бы их узнать зайдите на сайт и нажмите f12 -> network -> проголосуйте за любой пост -> в появившейся загрузке в пункте reqest headers будет ваша куки)

-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
save_var_ovr(var, name="new_pkl_file")

- сохраняет переменную с оверврайтом

save_var(var, name="new_pkl_file", __c=""):

- аналогичная функция но без оверврайта

load_var(file)

- загружает переменную

-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

parse_user_tag_list(user_page, fullname=False)

Парсит подписки юзера

- page страница пользователя

- fullname отключает basename

-- возвращает narray

-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


get_popular_tags(t="s", till=101)

  Получить список самых популярных тегов

- Первый аргумент  - | s = от количества подписок на тег | r = от рейтинга | (низходящий)
    
- до какой страницы сканировать (максимум 101)
    
-- возвращает [имена, количество постов в теге, количество подписок, рейтинг тега, ссылка на иконку тега] narray object
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
info_struct 

Глобальная структура хранящая переменные:

thread_num  - создает N количество потоков(субпроцессов) по дефолту эквивалентно количеству (физических ядер * логических ядер)

timeout = 1 - таймаут функции jp.parser 

d_path = os.path.join(os.path.expanduser("~"), "Downloads") - путь для скачивания по дефолту (${HOME}/Downloads)

cookie
