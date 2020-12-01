# Документация
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
page_max (page): - Определяет максимальное количество страниц

- Принимает страницу

-- возвращает int число
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
parser(page, from_page, until_page=0, on_text_tags=False, on_info=False)

- page - Первый аргумент это какая страница дожна быть просканирована| "://" обязателен, на конце не должно быть "/"
например http://joyreactor.cc/tag/котэ

- from_page - Второй аргумент получает цифру от какой страницы сканировать


- until_page - Третий аргумент получает цифру (по умолчанию 0)


- on_info -- пятый аргумент создает многомерный список с информацией о посте

    0 - теги 1 - рейтинги 2 - дата 3 - цифорки поста 4 - кол комментов 5 - лучшие комменты

    [tags,rating, date, keys, lencomments,bestcomments]

    по умолчанию выключен

    posttext -- парсит текст поста

    по умолчанию выключен

- posttext -- парсит текст поста

    по умолчанию выключен

-- Возвращает

return images, info, txt
    
-- 0 - многомерный список с картинками поста
    
-- 1 - многомерный список с многомерными списками с информацией
    
-- 2 - многомерный список с текстом
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
except_tag(linkbase=list, info=list, tagexceptions=list)
исключает нежелательные теги

- получает многомрный список изображений/текста

- получает масив с информацией[0] - индекс тегов

- список с исключениями которые вы выбераете, например [фурри, furry]

- spike: по умолчанию если все теги присудствуют то пост будет считаться засчитаным,
  если же вы поставите 1 то достаточно будет одного тега из заданного списка для того что бы пост засчитался
    
-- возвращает новый отсортированный список
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
sort_by_tag(linkbase=list, info=list, tagexceptions=list, spike = None):
 оставляет желательные теги

- linkbase: принимает многомрный список изображений/текста

- info: принимает масив с информацией[0] - индекс тегов

- tagexceptions: список с исключениями которые вы выбераете например [котэ, trap]

- spike: по умолчанию если все теги присудствуют то пост будет считаться засчитаным,
  если же вы поставите 1 то достаточно будет одного тега из заданного списка для того что бы пост засчитался
    
--  возвращает новый отсортированный список
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

sort_by_rate_comments
Сортировка по рейтингу/количеству комментов

- 1 Аргумент это что надо отсартировать картинки/текст

- 2 Аргумент переменная с информацией[индекс комментов/рейтинг]

- 3 Аргумент - цифра, ниже этого значения посты не пройдут

-- Возвращает list в порядке убывания
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
get_rdy(images)

- Принимает переменную с картинками после парса или после сортировки

Она просто переводит все ссылки в массив

-- Возвращает numpy array 1d


-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
download_images(images, download_path, warn_on=True)

- 1 Аргумент получает подготовленный get_rdy изображений

- 2 Аргумент в какую дирректорию надо скачивать

- 3 аргумент отключения предупреждений по уполчанию влючено

# Требования
Советую использовать conda 

- python 3.7

- requirements.txt

# Пример использования

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

jp.download_images(jp.get_rdy(jp.sort_by_rate_comments(linksbase, info[1], 0)), download_path=d_path)
```
