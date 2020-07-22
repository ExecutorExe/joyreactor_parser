import requests as req

from bs4 import BeautifulSoup as bs

import os.path
import time
import urllib.parse

links = []
tags = {}
y = []
p = []
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


#
#
#
#
# tag pars function(idn why idi i add it) to turn this function, tag_function value must be 1
tag_function = 0  # функция включения парса тегов файла(хз зачем добавил) чтобы включить значение должно быть равным: 1

d_path = r"E:\parser_data"  # куда сохранять? | dir to save

from_page = 75  # от какой страницы

till_page = 0  # до какой

website = "http://anime.reactor.cc/tag/Mikasa+Ackerman"  # какой сайт (без оканчания на "/")

print("website scan/index has started, please wait..."
      "\nсканирование/индексирование сайта началось, пожалуйста подождите...")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#
while not from_page == till_page:
    # не трогать блэт. сайт может забанить если запросов больше чем определенное значение
    # бан на какой то промежуток по ip вероятнее всего и может еще и по headers
    # фиксится библиотекой stem не я вам этого не говорил, и это не хорошо
    # возможно proxifier вместе с tor browser прокатит
    time.sleep(1)

    s = req.Session()
    # getting url
    url = s.get(website + "/" + str(from_page))
    print("scanning:", website + "/" + str(from_page), "\nэлементов найдено:", len(links))

    soup = bs(url.content, "html.parser")

    initdata = []


    # сам парсер

    def parser(soup, tagfunk=0):
        atr = ["a", "img"]  # "a" - большие изображения которые надо разворачивать + гифки
        # "img" - мелкие изображения которые слишком малы что бы разворачивать
        global ty
        data = []

        index = 0
        file_tag = {}
        # block selection
        for i in soup.select(".post_top"):
            # block selection
            for oo in i.select(".image"):
                # find all files
                # if file has "a" else this file has "ing"
                for i2 in oo.findAll(atr[index:]):
                    # print(atr[index:],i2)

                    if i2.has_attr("href"):
                        # decode urlencoded and add to list
                        data.append(urllib.parse.unquote(i2["href"]))
                        ty = i2["href"]
                        break

                    else:
                        # print(i2)
                        if i2.has_attr("src"):
                            ty = i2["src"]
                            # decode urlencoded and add to list
                            data.append(urllib.parse.unquote(i2["src"]))

                            break

                if tagfunk == 1:  # tag parser
                    # block selection
                    for ay in i.select(".taglist > b > a"):
                        # creating dict with tags
                        file_tag.setdefault(urllib.parse.unquote(os.path.basename(ty)), []).append("{}".format(ay.text))

        return data, file_tag


    from_page = from_page - 1  # counter

    # включаем парсер функцию
    x = parser(soup, tag_function)

    y, p = x
    # print(y)
    # создаем базу данных с линками
    links.extend(y)
    # создаем дикт с ключами имен файлов (без пути) это теги файлов
    tags.update(p)

    # print(tags)
    # b = list(set(b).union(y))
    # print(len(links),links)

# list1 = html.findAll("a", class_="prettyPhotoLink")
# list1.extend(html.findAll("a", class_="video_gif_source"))
# list1.extend(html.findAll("a", class_="video_gif_source"))

print("download startin...g\nначинаю загрузку...")
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# это данные которые передаются при запросе к link
# таким образом я обманываю сайт
request = ({
    'Host': 'img10.reactor.cc',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'image/webp,*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://anime.reactor.cc/',
    'Connection': 'keep-alive',

    'Cache-Control': 'max-age=0',
    'Pragma': 'no-cache'
})

#
for Im_link in links:  # итерация хуяция

    print("files left:", len(links) - 1)

    time.sleep(2)  # don't touch it coz ping need to not overload website or get wrecking ban
    # не трогать задержка нужна что бы не перегружать вэбсайт и не получить ебаный бан от сайта

    img_data = req.get(Im_link, headers=request).content

    with open(d_path + os.sep + os.path.basename(Im_link), 'wb') as handler:
        handler.write(img_data)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print("\n\n#===================================#")
print("# Code sequence successful complete #")
print("#===================================#")

# def my_function(x):
#    return list(dict.fromkeys(x))


__version__ = "Conda_env_3.7"
__author__ = "ExE https://github.com/ExecutorExe"
