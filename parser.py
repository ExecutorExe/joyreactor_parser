import requests as req

from bs4 import BeautifulSoup as bs

import os.path
import time
import urllib.parse

links = []
tags = {}
com = {}
inf = {}
y = []
p = []
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


#
#
#
infof = 0
# tag pars function(idn why idi i add it) to turn this function, tag_function value must be 1
tagf = 0  # функция включения парса тегов файла(хз зачем добавил) чтобы включить значение должно быть равным: 1

d_path = r"E:\parser_data"  # куда сохранять? | dir to save

from_page = 1631  # от какой страницы | например http://joyreactor.cc/user/rukanishu/35  (первую стриницу можно
# посмотреть снизу сайта)

till_page = 1630  # до какой | http://joyreactor.cc/user/rukanishu/1

website = "http://ar.reactor.cc"  # какой сайт (без оканчания на "/")

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

    soup = bs(url.content, "html.parser")

    initdata = []


    # сам парсер

    def parser(soup, tagfunk=0, tagf = 0, infof = 0):


        def info(i, ty,file_tag, path):
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
        global ty
        data = []
        rating_DMY_hm_postlink = {}
        bestcommenttext_userinfo_avatar_pic = {}
        index = 0
        file_tag = {}
        # block selection
        for i in soup.select(".article"):
            # print(i)

            for i2 in i.select(".post_content "):
                # print(i2)
                for i3 in i2.select(".image "):
                    # print(i3)
                    for i4 in i3.findAll(atr[index:]):
                        # print(atr[index:],i2)

                        if i4.has_attr("href"):
                            # print(i4)
                            # decode urlencoded and add to list
                            data.append(urllib.parse.unquote(i4["href"]))
                            ty = urllib.parse.unquote(os.path.basename(i4["href"]))
                            break

                        else:
                            # print(i2)
                            if i4.has_attr("src"):
                                ty = urllib.parse.unquote(os.path.basename(i4["src"]))
                                # decode urlencoded and add to list
                                data.append(urllib.parse.unquote(i4["src"]))

                            break
                    if tagf == 1:  # tag parser
                        # block selection


                        x = info(i, ty, ".post_top > .taglist > b > a")
                        file_tag = x
                    # дает некоторую информацию о посте


                    if infof == 1:
                        # рейтинг поста
                        x = info(i, ty,rating_DMY_hm_postlink, ".ufoot > div > .post_rating > span")
                        rating_DMY_hm_postlink = x
                        # дата  день год месяц точное время

                        x = info(i, ty,rating_DMY_hm_postlink ,".ufoot > div > .date > span > span")
                        rating_DMY_hm_postlink = x

                        # ссылка на пост
                        x = infolist(i, ty, rating_DMY_hm_postlink,"href", ".ufoot > div > .link_wr > a")
                        rating_DMY_hm_postlink = x

                        # лучший коммент (если он есть) тексты + имя юзеров  и тд + прикрепленные пикчи и аватары
                        x = info(i, ty, bestcommenttext_userinfo_avatar_pic,'.post_comment_list > div > div')
                        bestcommenttext_userinfo_avatar_pic = x

                        x = infolist(i, ty, bestcommenttext_userinfo_avatar_pic, "src", '.post_comment_list > div > div > img')
                        bestcommenttext_userinfo_avatar_pic = x



        return data, file_tag,bestcommenttext_userinfo_avatar_pic,rating_DMY_hm_postlink



    from_page = from_page - 1  # counter

    # включаем парсер функцию
    x = parser(soup,tagf,infof)

    y, p,c,h = x
    # print(y)
    # создаем базу данных с линками
    links.extend(y)
    # создаем дикт с ключами имен файлов (без пути) это теги файлов
    tags.update(p)
    com.update(c)
    inf.update(h)
    #print(len(tags))
    print("scanning:", website + "/" + str(from_page), "\nэлементов найдено:", len(links))

    # print(tags)
    # b = list(set(b).union(y))
    # print(len(links),links)

# list1 = html.findAll("a", class_="prettyPhotoLink")
# list1.extend(html.findAll("a", class_="video_gif_source"))
# list1.extend(html.findAll("a", class_="video_gif_source"))
if len(links) == 0:
    print("files does not found")
else:
    print("Download", len(links), "files?\n(y/n?)")
    x = input(":")
    if x.lower() == "y":
        print("download startin...g\nначинаю загрузку...")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

