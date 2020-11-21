# "Conda_env_3.7"
import os
import os.path
import time
import urllib.parse
import requests as rq  # '2.24.0'
from bs4 import BeautifulSoup as bs  # version '4.9.1'
from requests.exceptions import ConnectionError
import numpy as np  # 1.19.1
from numpy import array as araara  # :D
import re
import logging

# внимание, скорость монижена для того что бы не перегружать сервера сайта

# можно делать запросы следующим образом:
# http://joyreactor.cc/search?q=&user=&tags=котэ%2C+
# в этом запросе выводятся все посты где присудствует тэг "котэ" (но это не точно)
# запросы пишутся после "=", где:
# q - поиск(хз как он работает)
# user - автор поста
# tags - тэги (самый полезный запрос, выведутся  посты которые содержат данные теги)
# тэги пишутся через запятую где запятая в запросе это: %2C+
# обратите внимание что запросы начинаются с 1
# в отличие от конкретных тегов таких как joyreactor.cc/tag/котэ
# конкретные теги смотри на реакторе и в его фендомах (они раздиляются)


timeout = 1


# не трогать этот параметр блэт.
# сайт может забанить на какой то промежуток если запросов больше чем определенное значение
# если бы не это, то я бы использовал multiprocessing


def page_max(page):
    """

    :param page: принимает ссылку и проверяет сколько страниц
                 к примеру http://joyreactor.cc/tag/котэ
    :return: возвращает int число
    """
    temp = []
    try:
        # s = rq.Session()
        soup = bs(rq.get(page).content, "html.parser")
        for i in soup.findAll(class_="pagination_expanded"):
            for i0 in i.findAll(["a"]):
                temp.extend(map(int, i0(text=True)))
            for i1 in i.findAll("span", {'class': "current"}):
                temp.extend(map(int, i1(text=True)))

        return max(temp)
    except ConnectionError:
        print("<<!alert, connection error!>>")
        # sleep for a bit in case that helps
        # try again
        time.sleep(2)
        print("<<trying to reconnect>>")
        return page_max(page)
    except ValueError as e:
        if "/post/" in page or "/tag/" in page or "/user/" in page:
            return 1
        else:
            raise e


def parser(page, from_page, until_page=0, on_info=False, posttext=False):
    """

    Input:
    ------
    -- parser(page, from_page, until_page=0, on_info=False,posttext=False )

    -page -- первый аргумент это какая страница дожна быть просканирована|
    "://" обязателен, на конце не должно быть "/"
    например http://joyreactor.cc/tag/Sakimichan

    from_page -- второй аргумент получает цифру от какой страницы сканировать


    -until_page -- третий аргумент получает цифру (по умолчанию 0)


    -on_info -- пятый аргумент создает многомерный список с информацией о посте

    0 - теги 1 - рейтинги 2 - дата 3 - цифорки поста 4 - кол комментов 5 - лучшие комменты

    [tags,rating, date, keys, lencomments,bestcomments]

    по умолчанию выключен

    -posttext -- парсит текст поста

    по умолчанию выключен





    Output:
    -------
    return images,info, txt

    0 - многомерный список с картинками поста

    1 - многомерный список с многомерными списками с информацией

    2 - многомерный список с текстом


    """
    if "reactor.cc/search" in page:
        if "q=&" in page:
            page = page.replace("q=&", "")
        if "user=&" in page:
            page = page.replace("user=&", "")
        sl = page.split("search", 2)
        search = True
    else:
        search = False

    # сразу извиняюсь, на этом проекте я учился использовать bs4(я не читал док)
    def getpage(page, from_page):
        try:
            # s = rq.Session(page)
            # getting url
            url = rq.get(page)
            return url
        except ConnectionError:
            print("<<!alert, connection error!>>")
            # sleep for a bit in case that helps
            input("><to reconnect type anything><")

            # try again
            return getpage(page, from_page)

    def info(i, path):
        temp = []
        for ay in i.select(path):
            # creating dict with tags
            temp.append(ay.text)
        return temp

    rating = []
    date = []
    bestcomments = []
    lencomments = []
    keys = []
    txt = []
    images = []
    tags = []

    while not from_page == until_page:
        if search:
            page_ind = sl[0] + "search/+/" + str(from_page) + sl[1]
        else:
            page_ind = page + "/" + str(from_page)

            print(page_ind)
        soup = bs(getpage(page_ind, from_page).content, "html.parser")

        temptext = []
        tempdate = []
        temprating = []
        tempkey = []
        temptags = []
        templencom = []
        tempbestcom = []

        # block selection
        for i in soup.select(".article.post-normal"):
            # create post number as dict key

            datatext = []
            if posttext:
                # парс текста в посте если он имеется
                for io in i.select(".post_content > div"):
                    if io.text:
                        datatext.append(io.text)

            if on_info:
                # теги

                temptags.append(info(i, ".post_top > .taglist > b > a"))
                # рейтинг поста
                # temprating.append(info(i, ))
                # temp = []
                for ay in i.select(".ufoot > div > .post_rating > span"):
                    # creating dict with tags
                    try:
                        temprating.append(float(ay.text))
                    except ValueError as e:
                        print(e)
                        logging.error("<<!>>connect to VPN<<!>>")
                        exit()

                # дата  день год месяц точное время
                tempdate.append(info(i, ".ufoot > div > .date > span > span"))

                # ссылка на пост
                for ay in i.select(".ufoot > div > .link_wr > a"):
                    tempkey.append(os.path.basename(ay["href"]))

                # лучший коммент (если он есть) тексты + имя юзеров  и тд + прикрепленные пикчи и аватары
                tempbestcom.append(info(i, '.post_comment_list > div > div'))

                for ay in i.select('.commentnum.toggleComments'):
                    # creating dict with tags

                    templencom.extend((re.findall(r'\d+', ay.text)))

            dataimage = []
            for i0 in i.select(".post_content"):
                for i1 in i0.select(".image"):
                    # print(i3)
                    # "a" - большие изображения которые надо разворачивать + гифки
                    # "img" - мелкие изображения которые слишком малы что бы разворачивать
                    for i2 in i1.findAll(["a", "img"][:]):
                        # парс исзображения
                        if i2.has_attr("href"):
                            # decode urlencoded and add to list
                            dataimage.append(urllib.parse.unquote(i2["href"]))

                            break

                        else:
                            # если нет достаточно крупного изображения
                            if i2.has_attr("src"):
                                # decode urlencoded and add to list
                                dataimage.append(urllib.parse.unquote(i2["src"]))

                            break
            images.append(dataimage)
            temptext.append(datatext)

        from_page -= 1

        rating.extend(temprating)
        lencomments.extend(templencom)
        txt.extend(temptext)
        tags.extend(temptags)
        bestcomments.extend(tempbestcom)
        keys.extend(tempkey)
        date.extend(tempdate)

        time.sleep(timeout)
    # print(temptext)
    info = [tags, rating, date, keys, araara(lencomments).astype(dtype=int), bestcomments]
    return images, info, txt


# Saving the objects:


def sort_by_rate_comments(linksbase, info_index, rating=0):
    """
    Рейтинг = imfo[1] | Комменты - imfo[4]


    :param linksbase: 1 аргумент это что надо отсартировать картинки/текст
    :param info: 2 аргумент переменная с информацией
    :param rating: 3 аргумент - цифра, ниже этого значения посты не пройдут
    :return: список с удаленными в них постами ниже определенного рейтинга
    """

    sorted_links = []
    idexes = np.argsort(info_index)[::-1]
    for i, v in enumerate(araara(info_index)[idexes]):
        if v < rating:
            break
        sorted_links.append(linksbase[idexes[i]])

    return sorted_links


def except_tag(linkbase=list, info=list, tagexceptions=list, spike=None):
    """

    :param linkbase: принемает многомрный список изображений/текста
    :param info: принемает масив с информацией
    :param tagexceptions: список с исключениями которые вы выбераете например [фурри, furry]
    :param spike: по умолчанию если все теш=ги присудствуют то пост будет считаться
    засчитаным, если же вы поставите 1 то достаточно будет одного тега для того что бы пост прошел
    :return: возвращает новый отсортированный список
    """
    if spike is None:
        spike = len(tagexceptions)

    sortedlist = []

    for i, v in enumerate(info[0]):
        counter = 0
        for i0 in tagexceptions:
            if i0 in v:
                counter = counter + 1
            if counter != spike and i0 == tagexceptions[-1]:
                sortedlist.append(linkbase[i])

    return sortedlist


def sort_by_tag(linkbase=list, info=list, tagexceptions=list, spike=None):
    """

    :param linkbase: принемает многомрный список изображений/текста
    :param info: принемает масив с информацией
    :param tagexceptions: список с исключениями которые вы выбераете например [фурри, furry]
    :param spike: по умолчанию если все теш=ги присудствуют то пост будет считаться
    засчитаным, если же вы поставите 1 то достаточно будет одного тега для того что бы пост прошел
    :return: возвращает новый отсортированный список

    """
    if spike is None:
        spike = len(tagexceptions)

    sortedlist = []

    for i, v in enumerate(info[0]):
        counter = 0
        for i0 in tagexceptions:
            if i0 in v:
                counter = counter + 1
            if counter == spike:
                sortedlist.append(linkbase[i])
                break
    return sortedlist


def get_rdy(images):
    """

    :param images: принимает list с картинками что бы подготовить к скачиванию
    :return: возвращает одномерный numpy массив
    """
    try:
        val = np.concatenate(images).ravel()
        # если пост
        i = np.where(val == "javascript:")
        if i[0]:
            val = np.delete(val, i)
        return val
    except ValueError:
        return []


def parse_user_tag_list(page):
    temp = []
    try:
        # s = rq.Session()
        soup = bs(rq.get(page).content, "html.parser")
        for i in soup.select(".sidebar_block.blogs_wr > .sidebarContent"):
            for i0 in i.findAll(["a"]):
                temp.append(urllib.parse.unquote(i0["href"]))
        return temp
    except ConnectionError:
        print("<<!alert, connection error!>>")
        # sleep for a bit in case that helps
        # try again
        time.sleep(2)
        print("<<trying to reconnect>>")
        return page_max(page)


def download_images(images, download_path, warn_on=True):
    """

    :param images: 1 аргумент принемает подготовленный список изображений (get_rdy(images) просто вставьте это)

    :param download_path: 2 аргумент в какую дирректорию надо скачивать

    :param warn_on: 3 аргумент отключения предупреждений по уполчанию влючено

    """

    def downloader(links, d_path):

        # это данные которые передаются при запросе к link
        # таким образом я избавляюсь от ватермарки сайта

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

        # функция если у вас проблемы с интеренетом
        def getimage(Im_link, request, path_FileBaseName):
            try:
                time.sleep(timeout)  # don't touch it coz ping need to not overload website or get frecking ban
                # не трогать задержка нужна что бы не перегружать вэбсайт и не получить ебаный бан от сайта
                with open(path_FileBaseName, 'wb') as f:  # открываем файл
                    f.write(rq.get(Im_link, headers=request).content)
                    # делаем запрос на получение файла

            except ConnectionError as e:
                if warn_on:

                    print("<<!alert, connection error!>>")
                    # sleep for a bit in case that helps
                    input("><to reconnect type anything><")
                    # try again
                    return getimage(Im_link, request, path_FileBaseName)
                else:
                    raise e

        for Im_link in links:  # итерация хуяция
            if warn_on:
                print("<< files left:", counter, ">>")
            counter = counter - 1

            path_FileBaseName = d_path + os.sep + os.path.basename(Im_link)
            # проверяем существует ли файл в диооектории

            if not os.path.exists(path_FileBaseName):

                getimage(Im_link, request, path_FileBaseName)
            else:
                if warn_on:
                    print("<<!File (" + os.path.basename(Im_link) + ") already existing in dir (" + d_path + ")!>>")

    # эта функция интуитивно понятна
    if warn_on:
        if len(images) == 0:
            print("<<files does not found>>")
        else:
            print("\n<<Download", len(images), "files?>>\n")
            x = input("><Proceed ([y]/n)?><")
            if x.lower() == "y":
                downloader(images, download_path)
            elif x.lower() == "n":
                print("<<exiting>>")
            else:
                print("><!Input value is incorrect, try again.!><\n[y - Yes]\n[n - No]")
                download_images(images, download_path)

    else:
        downloader(images, download_path)


__author__ = "ExE https://github.com/ExecutorExe"
