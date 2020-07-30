# "Conda_env_3.7"
import requests as req
from bs4 import BeautifulSoup as bs
import os.path
import time
import urllib.parse
import pickle
links = []
data_text = {}
tags = {}
com = {}
inf = {}
sorted_links = ([])
linksbase = {}
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# SETTINGS | ПАРАМЕТРЫ
# не забудьте включить vpn для пк(vpngate к примеру, он бесплатный)

ratingf = 1  # включение-1 выключение-0 функции сортировки по рейтингу поста infof тоже должна быть включена
rating = 60  # все посты выше этого значения будут скачены

infof = 1  # индексирует пачку информации для каждой ссылки

# tag pars function to turn this function, tag_function value must be 1
tagf = 0  # функция включения парса тегов файла(хз зачем добавил) чтобы включить значение должно быть равным: 1
# tagf так же включает парс текста в посте если он имеется

d_path = r"E:\parser_data"  # куда сохранять? | dir to save

from_page = 4979  # от какой страницы | например http://joyreactor.cc/user/rukanishu/35  (первую стриницу можно
# посмотреть снизу сайта)
from_page_pickle = from_page
till_page = 1  # до какой | http://joyreactor.cc/user/rukanishu/1

page = "http://anime.reactor.cc/tag/ecchi"
# какая пейджа  пример http://joyreactor.cc/best(без оканчания на "/")
# http:// - обязательно
# в ссылке не должно быть подобных символов %D0%AD%D1%82%D1%82%D0%B8

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


print("website scan/index has started, please wait..."
      "\nсканирование/индексирование сайта началось, пожалуйста подождите...")
#
while not from_page == till_page:
    # не трогать блэт. сайт может забанить если запросов больше чем определенное значение
    # бан на какой то промежуток по ip вероятнее всего и может еще и по headers(это переменная request)
    # фиксится библиотекой stem не я вам этого не говорил, и это не хорошо
    # возможно proxifier вместе с tor browser прокатит
    time.sleep(1)
    ccc = 0


    def getpage(page,from_page):
        try:
            s = req.Session()
            # getting url
            url = s.get(page + "/" + str(from_page))
            return url
        except Exception:
            print("упс, похоже что то произошло интернетом, пожалуста проверьте соединение и переподключитесь к впн")
            # sleep for a bit in case that helps
            input("для переподключения введите все что угодно:")
            # try again
            return getpage(page,from_page)


    soup = bs(getpage(page,from_page).content, "html.parser")


    # сам парсер

    def parser(soup, tagf=0, infof=0):

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

        atr = ["a", "img"]  # "a" - большие изображения которые надо разворачивать + гифки
        # "img" - мелкие изображения которые слишком малы что бы разворачивать
        global key
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

    print("scanning:", page + "/" + str(from_page), "\nposts scanned:", len(linksbase.values()))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# создаем сохранение переменной

with open(os.path.basename(page)+"_pic"+"("+str(from_page_pickle)+"-"+str(till_page)+")"+".pkl", 'wb') as f:
    pickle.dump(linksbase, f)
with open(os.path.basename(page) + "_info" + "(" + str(from_page_pickle) + "-" + str(till_page) + ")" + ".pkl", 'wb') as f:
    pickle.dump(inf, f)
# пример применения функции инфо - сортировка по рейтингу


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print("\n\n#===================================#\n# Code sequence successful complete #"
      "\n#===================================#")

# def my_function(x):
#    return list(dict.fromkeys(x))


__version__ = "0.1"
__author__ = "ExE https://github.com/ExecutorExe"
