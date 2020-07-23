import requests as req
from bs4 import BeautifulSoup as bs
import os.path
import time
import urllib.parse

image_counter = 0
links = []
data_text = {}
tags = {}
com = {}
inf = {}
y = []
p = []
sorted_links = []
linksbase = {}
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# SETTINGS | ПАРАМЕТРЫ

ratingf = 0  # включение-1 выключение-0 функции сортировки по рейтингу поста infof тоже должна быть включена
rating = 30  # все посты выше этого значения будут скачены

infof = 0  # индексирует пачку информации для каждой ссыолки

# tag pars function(idn why idi i add it) to turn this function, tag_function value must be 1
tagf = 0  # функция включения парса тегов файла(хз зачем добавил) чтобы включить значение должно быть равным: 1
# tagf так же включает парс текста в посте если он емеется 
d_path = r"E:\parser_data"  # куда сохранять? | dir to save

from_page = 5724  # от какой страницы | например http://joyreactor.cc/user/rukanishu/35  (первую стриницу можно
# посмотреть снизу сайта)

till_page = 5720  # до какой | http://joyreactor.cc/user/rukanishu/1

website = "http://joyreactor.cc/discussion/flame"  # какая пейджа  пример http://joyreactor.cc/best(без оканчания на "/"
# http:// - обязательно

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


print("website scan/index has started, please wait..."
      "\nсканирование/индексирование сайта началось, пожалуйста подождите...")
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

    soup = bs(url.content, "html.parser")

    initdata = []


    # сам парсер

    def parser(soup, tagf=0, infof=0):
        """
        def info(i, ty, file_tag, path):
            for ay in i.select(path):
                # creating dict with tags
                file_tag.setdefault(ty, []).append("{}".format(ay.text))
            return file_tag"""

        # def infolist(i, file_tag, atr, path):

        # creating dict with tags
        # print(ay[atr])

        # return file_tag

        atr = ["a", "img"]  # "a" - большие изображения которые надо разворачивать + гифки
        # "img" - мелкие изображения которые слишком малы что бы разворачивать
        global key, image_counter
        data = []

        datatext = {}
        dataimage = {}
        rating_DMY_hm_postlink = {}
        bestcommenttext_userinfo_avatar_pic = {}
        index = 0
        file_tag = {}
        # block selection
        for i in soup.select(".article"):
            # create post number as dict key
            for ay in i.select(".ufoot > div > .link_wr > a"):
                key = os.path.basename(ay["href"])

            def info(i, ty, file_tag, path):
                for ay in i.select(path):
                    # creating dict with tags
                    file_tag.setdefault(ty, []).append("{}".format(ay.text))
                return file_tag

            def infolist(i, ty, file_tag, atr, path):
                for ay in i.select(path):
                    # creating dict with tags
                    file_tag.setdefault(ty, []).append("{}".format(ay[atr]))
                return file_tag

            # print(i)

            for i2 in i.select(".post_content "):

                
                if tagf == 1:
                    # парс текста в посте если он имеется 
                    for io in i2.select("div"):
                        if io.text:
                            datatext.setdefault(key, []).append("{}".format(io.text))
                    # tag parser
                    # block selection

                    x = info(i, key, file_tag, ".post_top > .taglist > b > a")
                    file_tag = x
                if infof == 1:
                    # рейтинг поста
                    x = info(i, key, rating_DMY_hm_postlink, ".ufoot > div > .post_rating > span")
                    rating_DMY_hm_postlink = x
                    # дата  день год месяц точное время

                    x = info(i, key, rating_DMY_hm_postlink, ".ufoot > div > .date > span > span")
                    rating_DMY_hm_postlink = x

                    # ссылка на пост

                    # лучший коммент (если он есть) тексты + имя юзеров  и тд + прикрепленные пикчи и аватары
                    x = info(i, key, bestcommenttext_userinfo_avatar_pic, '.post_comment_list > div > div')
                    bestcommenttext_userinfo_avatar_pic = x

                    x = infolist(i, key, bestcommenttext_userinfo_avatar_pic, "src",
                                 '.post_comment_list > div > div > img')
                    bestcommenttext_userinfo_avatar_pic = x

                # print(i2)
                for i3 in i2.select(".image "):
                    # print(i3)
                    for i4 in i3.findAll(atr[index:]):
                        # print(atr[index:],i2)

                        if i4.has_attr("href"):
                            # print(i4)
                            # decode urlencoded and add to list
                            dataimage.setdefault(key, []).append("{}".format(urllib.parse.unquote(i4["href"])))

                            break

                        else:
                            # print(i2)
                            if i4.has_attr("src"):
                                # decode urlencoded and add to list
                                dataimage.setdefault(key, []).append("{}".format(urllib.parse.unquote(i4["src"])))

                            break

                    # дает некоторую информацию о посте

        return dataimage, datatext, file_tag, bestcommenttext_userinfo_avatar_pic, rating_DMY_hm_postlink


    from_page = from_page - 1  # counter

    # включаем парсер функцию
    x = parser(soup, tagf, infof)

    y, p, c, h, b = x
    # print(y)
    # создаем базу данных с линками
    # извлекаем ссылки на пикчи (номер_поста:[картанка1, картинка2])
    linksbase.update(y)
    # извлекаем текст
    data_text.update(p)
    # создаем дикт с ключами номера поста  это теги файлов
    tags.update(c)
    # лучшие коменты и тд
    com.update(h)
    # пачка информации о посте 
    inf.update(b)

    print("scanning:", website + "/" + str(from_page), "\nposts scanned:", len(linksbase.values()))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# пример применения функции инфо - сортировка по рейтингу
if ratingf == 1:
    print("sorting by rating...")
    for me in linksbase:
        if float(inf[me][0]) >= rating:
            sorted_links.extend(linksbase[me])
    links = sorted_links

else:
    for link in linksbase.values():
        links.extend(link)

# def duplicate(x):
#   print(len(list(dict.fromkeys(x))))


# return list(dict.fromkeys(x))

if len(links) == 0:
    print("files does not found")
else:
    print("\n\nDownload", len(links), "files?\n\n")
    x = input("Proceed ([y]/n)?\n\n")
    if x.lower() == "y":
        print("download starting...\nначинаю загрузку...")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # это данные которые передаются при запросе к link
        # таким образом я обманываю сайт

        request = ({
            'Host': 'img10.reactor.cc',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'image/webp,*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://joyreactor.cc/',
            'Connection': 'keep-alive',

            'Cache-Control': 'max-age=0',
            'Pragma': 'no-cache'
        })

        counter = int(len(links))

        for Im_link in links:  # итерация хуяция

            print("files left:", counter)
            counter = counter - 1

            time.sleep(2)  # don't touch it coz ping need to not overload website or get wrecking ban
            # не трогать задержка нужна что бы не перегружать вэбсайт и не получить ебаный бан от сайта

            # проверяем существует ли файл в диооектории
            if not os.path.exists(d_path + os.sep + os.path.basename(Im_link)):
                with open(d_path + os.sep + os.path.basename(Im_link), 'wb') as handler:  # открываем файл
                    handler.write(req.get(Im_link, headers=request).content)  # делаем запрос на получение файла

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print("\n\n#===================================#\n# Code sequence successful complete #"
      "\n#===================================#")

# def my_function(x):
#    return list(dict.fromkeys(x))


__version__ = "Conda_env_3.7"
__author__ = "ExE https://github.com/ExecutorExe"
