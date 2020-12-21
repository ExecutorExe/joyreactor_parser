# Требования
Советую использовать conda 

- python 3.7

- [requirements.txt](https://github.com/ExecutorExe/joyparser/blob/master/requirements.txt)


# Документация
page_max (page): - Определяет максимальное количество страниц

- Принимает страницу

-- возвращает int число
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
parser(page, from_page, until_page=0, on_text_tags=False, on_info=False)

- page - Первый аргумент это какая страница дожна быть просканирована| "://" обязателен, на конце не должно быть "/"
например http://joyreactor.cc/tag/котэ

- from_page - Второй аргумент получает цифру от какой страницы сканировать


- until_page - Третий аргумент получает цифру до какой страницы сканировать (по умолчанию 0)


- posttext -- парсит текст поста и лучшие комменты

    по умолчанию выключен

-- Возвращает

return images, info, txt
    
-- 0 - многомерный список с картинками поста
    
-- 1 - многомерный список с многомерными списками с информацией  [tags,rating, date, keys, lencomments]
    
-- 2 - многомерный список с текстом и лучшими комментами

Пример:
```python
import joyparser as jp

till_page = 0  # до какой | http://joyreactor.cc/user/котэ/1
#
page = "http://joyreactor.cc/tag/котэ"
# какая пейджа  пример http://joyreactor.cc/котэ (без оканчания на "/")

d_path = r"D:\parser_data"

from_page = 1
# от какой страницы | например http://joyreactor.cc/user/котэ/35 
# или воспользуйтесь jp.page_max(page) эта функция вернет максимальное количество страниц

linksbase, info, txt = jp.parser(page, from_page, 0, on_info=True)

jp.download_images(jp.get_rdy(jp.get_val_by_index(linksbase,jp.sort_by_rate_comments(info[1], download_path=d_path)
```
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
sort_by_tag(info=list, tagexceptions=list, spike=None)
     индекс тегов - info[0]


   - info: принемает масив с информацией
   
   - tagexceptions: список с исключениями которые вы выбераете например [хоба!, anime]
   
   - spike: по умолчанию если все теги присудствуют то пост будет считаться
    засчитаным, если же вы поставите 1 то достаточно будет одного тега для того что бы пост прошел
    
   -- возвращает новый отсортированный список индексов
```python
import numpy as np 
import joyparser as jp

value = np.array([[1,2,3,4],
                  [11,22,33,44],
                  [111,222,333,444]])
indexes = np.array([10,5,7])
print(value[jp.sort_by_tag(value,[1,2])])
#output [[1 2 3 4]]
print(value[jp.sort_by_tag(value,[1,2,44])])
#IndexError: arrays used as indices must be of integer (or boolean) type
# потому что нет результатов от все трех запрашиваемых значений
print(value[jp.sort_by_tag(value,[1,2,44],spike=1)])
#output
#[[ 1  2  3  4]
# [11 22 33 44]]
```
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
def except_tag(info=list, tagexceptions=list, spike=None)
    
   индекс тегов - info[0]

 - info: принемает масив с информацией
 
 - tagexceptions: список с исключениями которые вы выбераете например [фурри, furry]
 
 - spike: по умолчанию если все теги присудствуют то пост будет считаться
    засчитаным в исключение, если же вы поставите 1 то достаточно будет одного тега для того что бы пост попал в исключение
    
 -- возвращает индексы
 
 Все тоже самое что и sort_by_tag просто исключения тегов
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
def sort_by_rate_comments(info_index, rating=0)
    
   Рейтинг = imfo[1] | Комменты - imfo[4]

 - info: 1 аргумент переменная с информацией
 
 - rating: 2 аргумент - цифра, ниже этого значения посты не пройдут
 
 -- отсортированные индексы
 
 Пример:
 ```python
import numpy as np
import joyparser as jp

value = np.array([[1,2,3,4],
                  [11,22,33,44],
                  [111,222,333,444]])
indexes = np.array([10,5,7])
print(value[jp.sort_by_rate_comments(indexes,6)])

#output
#[[  1   2   3   4]
# [111 222 333 444]]
# или можно воспользоваться np.where 

print(value[np.where(indexes>=6)])

#output
#[[  1   2   3   4]
# [111 222 333 444]]
```
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
def get_val_by_index(value, index):
    
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
download_images(images, download_path, warn_on=True)

- 1 Аргумент получает подготовленный get_rdy изображений

- 2 Аргумент в какую дирректорию надо скачивать

- 3 аргумент отключения предупреждений по уполчанию влючено True/False
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
def votegun(posts_array, cookie, token, vote=True, __abyss="0")

плюсо/минусо-мет
(просьба не злоупотреблять этой функцией)

- posts_array: номера постов(одномерный масив)
  
- cookie: куки(что бы их узнать зайдите на сайт и нажмите f12 -> network -> проголосуйте за любой пост -> в появившейся загрузке в пункте reqest headers будет ваша куки)

- token: все тоже самое что и с куки, в самом низу должен быть токен

- vote: голосует за или против(True/False)

-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
save_var_ovr(var, name="new_pkl_file")

- сохраняет переменную с оверврайтом

save_var(var, name="new_pkl_file", __c=""):

- аналогичная функция но без оверврайта

load_var(file)

- загружает переменную




