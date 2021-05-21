# "Conda_env_3.7"
import os
import os.path
import sys
import time
import urllib.parse
import requests as rq  # '2.24.0'
from bs4 import BeautifulSoup as bs  # version '4.9.1'
from requests.exceptions import ConnectionError
import numpy as np  # 1.19.1
from numba import njit  # 0.51.2
import re
import pickle
from multiprocessing import cpu_count  # GIL is shit
from concurrent.futures import ThreadPoolExecutor

# openmp <3

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
messages = np.array(["<<!alert, connection error!>>",
                     "><to reconnect type anything><",
                     "<<trying to reconnect>>",
                     "<<files does not found>>"])


class info_struct:
    thread_num = cpu_count()
    timeout = 1
    d_path = os.path.join(os.path.expanduser("~"), "Downloads")
# DRY -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#-

@njit
def uni(array, leng, empty_array):
    """
    unique
    empty_array[:count]
    :param array:
    :param leng:
    :param empty_array:
    :return:
    """
    count = 1
    empty_array[0] = 0
    for i in range(1, leng):
        state = True
        for j in range(count):
            if array[i] == array[empty_array[j]]:
                state = False
                break
        if state:
            empty_array[count] = i
            count = count + 1
    return count

def mtdownloader(links):
    """
    single (master) thread donwnloader
    """
    # why i can't just 
    # #pragma omp parallel for
    # in python 
    for i in links:
        getimage(i)

def mpdownloader(links):
    """
    create N workers(processes) for function 
    # why i can't just 
    # #pragma omp parallel for
    # in python """
    with ThreadPoolExecutor(max_workers=info_struct.thread_num) as p:
        p.map(getimage,links)



def getpage(page):
    try:
        # getting url
        url = rq.get(page)
        return url
    except ConnectionError:
        print(messages[0])
        input(messages[1])

        # try again
        return getpage(page)


def get_info(i, path):
    temp = []
    for ay in i.select(path):
        temp.append(ay.text)
    return temp


def getimage(Im_link):
    request = ({
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'img1.joyreactor.cc',
        'Referer': 'http://joyreactor.cc/',
    })
    request["Host"] = Im_link[7:12] + ".joyreactor.cc"
    path_FileBaseName = info_struct.d_path + os.sep + os.path.basename(Im_link)
    # проверяем существует ли файл в диооектории
    if not os.path.exists(path_FileBaseName):
        try:

            with open(path_FileBaseName, 'wb') as f:  # открываем файл
                f.write(rq.get(Im_link, headers=request).content)
                # делаем запрос на получение файла

        except Exception as e:
            if (os.path.isfile(path_FileBaseName)):
                os.remove(path_FileBaseName)
            raise e


# END_DRY -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#-

def page_max(page: str):
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
        print(messages[0])
        # sleep for a bit in case that helps
        # try again
        time.sleep(2)
        print(messages[2])
        return page_max(page)
    except ValueError as e:
        if "/post/" in page or "/tag/" in page or "/user/" in page or "/search/" in page:
            return 1
        else:
            raise e


def search(base="joyreactor", search=[], tags=[], user=[]):
    """
    Делает поиск

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

	:param base: базовое имя фендом и т.д
    :param search: просто поиск хз как он работает list
    :param tags: теги list
    :param user: пользователь list
    :return: page str
    """
    return "http://" + base + ".cc/search?q={}".format("%2C+".join(search)) + \
           "&user={}".format("%2C+".join(user)) + "&tags=" + "{}".format("%2C+".join(tags)) + "&"


def parser(page: str, from_page: int, until_page=0, update_parsed_array=None):
    """
    парсер может сканировать теги or основные страницы по типу best or юзеров одиночные посты or поисковые запросы

    Input:
    ------
    -- parser(page, from_page, until_page=0, on_info=False,posttext=False )

    -page -- первый аргумент это какая страница дожна быть просканирована|
    "://" обязателен, на конце не должно быть "/"
    например http://joyreactor.cc/tag/Sakimichan

    -from_page -- второй аргумент получает цифру от какой страницы сканировать

    -until_page -- третий аргумент получает цифру (по умолчанию 0)

    -posttext -- парсит текст поста и лучших комментов по умолчанию выключен(не обязательный аргумент)

    -update_parsed_array принимает уже отпарсеный список и обновит до первого совпавшего поста(не обязательный аргумент)
    если обновлений не найдено возвращает None

    Output:
    -------
    [images,
    [tags,rating,date,keys],
    [len_comments,text,bestcomments]]
    """

    if update_parsed_array is None:
        upd = False
    else:

        upd = True

    if from_page == int:  # default setting if no custom numbers
        from_page = page_max(page)

    if "reactor.cc/search" in page:  # if search
        if "q=&" in page:
            page = page.replace("q=&", "")
        if "user=&" in page:
            page = page.replace("user=&", "")
        sl = page.split("search", 2)
        search = True
    else:
        search = False

    # сразу извиняюсь, на этом проекте я учился использовать bs4(я не читал док)

    rating = []
    date = []
    bestcomments = []
    lencomments = []
    keys = []
    txt = []
    images = []
    tags = []

    # print(len(images),len(tags), len(rating),len(date),len(lencomments))

    while not from_page == until_page:
        if search:
            page_ind = sl[0] + "search/+/" + str(from_page) + sl[1]
        else:
            page_ind = page + "/" + str(from_page)

            sys.stdout.write("<< pages left: " + str(from_page - until_page) + " >>\0\r")
        soup = bs(getpage(page_ind).content, "html.parser")

        temptext = []
        tempdate = []
        temprating = []
        tempkey = []
        temptags = []
        templencom = []
        tempbestcom = []

        # block selection
        for i in soup.select(".article.post-normal"):

            datatext = []
            # парс текста в посте если он имеется
            for io in i.select(".post_content > div"):
                if io.text:
                    datatext.append(io.text)

                    # лучший коммент (если он есть) тексты + имя юзеров  и тд + прикрепленные пикчи и аватары
                tempbestcom.append(get_info(i, '.post_comment_list > div > div'))

            temptags.append(get_info(i, ".post_top > .taglist > b > a"))
            # рейтинг поста

            for ay in i.select(".ufoot > div > .post_rating > span"):
                # creating dict with tags
                try:
                    temprating.append(float(ay.text))
                except ValueError as e:
                    sys.stderr.write("<<!>>connect to VPN<<!>>\n")
                    input("><to reconnect type anything><")

                    # try again
                    return parser(page, from_page, until_page, update_parsed_array)
                    # exit()

            # дата  день год месяц точное время
            tempdate.append(get_info(i, ".ufoot > div > .date > span > span"))

            # ссылка на пост
            for ay in i.select(".ufoot > div > .link_wr > a"):
                tempkey.append(os.path.basename(ay["href"]))

            for ay in i.select('.commentnum.toggleComments'):
                # creating dict with tags

                templencom.extend((re.findall(r'\d+', ay.text)))

            dataimage = []
            for i0 in i.select(".post_content"):
                for i1 in i0.select(".image"):
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
        if upd:
            for post_number in range(len(tempkey)):
                if np.uint32(tempkey[post_number]) == update_parsed_array[1][3][0]:
                    print("<< Found element[0] at ", tempkey[post_number], " >>")

                    len_arr = len(keys)
                    keys = np.array(keys, dtype=np.uint32)
                    indices = np.empty(len_arr, dtype=np.uint32)
                    end_index = uni(keys, len_arr, indices)
                    indices = indices[:end_index]

                    if len(keys) == 0:
                        print("<< No updates found >>")
                        return None
                    else:
                        sys.stdout.write("\n")
                        return np.append(np.array(images, dtype=object)[indices], update_parsed_array[0]), \
                               [np.append(np.array(tags, dtype=object)[indices], update_parsed_array[1][0]),
                                np.append(np.array(rating, dtype=np.float32)[indices], update_parsed_array[1][1]),
                                np.append(np.array(date, dtype=object)[indices], update_parsed_array[1][2]),
                                np.append(keys[indices], update_parsed_array[1][3]),
                                np.append(np.array(lencomments, dtype=np.uint32)[indices], update_parsed_array[1][4])], \
                               [np.append(np.array(txt, dtype=object)[indices], update_parsed_array[2][0]),
                                np.append(np.array(bestcomments, dtype=object)[indices], update_parsed_array[2][1])]

                else:
                    rating.append(temprating[post_number])
                    lencomments.append(templencom[post_number])
                    txt.append(temptext[post_number])
                    tags.append(temptags[post_number])
                    bestcomments.append(tempbestcom[post_number])
                    keys.append(tempkey[post_number])
                    date.append(tempdate[post_number])
            time.sleep(info_struct.timeout)

        else:
            rating.extend(temprating)
            lencomments.extend(templencom)
            txt.extend(temptext)
            tags.extend(temptags)
            bestcomments.extend(tempbestcom)
            keys.extend(tempkey)
            date.extend(tempdate)
            time.sleep(info_struct.timeout)

    keys = np.array(keys, dtype=np.uint32)
    # избавляемся от дубликатов если они есть
    # нет не мог использовать словари, патаму шо медленные и numpy one love
    len_arr = len(keys)
    indices = np.empty(len_arr, dtype=np.uint32)
    end_index = uni(keys, len_arr, indices)
    indices = indices[:end_index]

    sys.stdout.write("\n")
    return \
        np.array(images, dtype=object)[indices], \
        [np.array(tags, dtype=object)[indices],

         np.array(rating, dtype=np.float32)[indices],
         np.array(date, dtype=object)[indices],
         keys[indices],

         np.array(lencomments, dtype=np.uint32)[indices]], \
        [np.array(txt, dtype=object)[indices], np.array(bestcomments, dtype=object)[indices]]


def parse_page(page: str):
    """
    Parse single page(dev version)
    :param page: pagename example: http://joyreactor.cc
    :return:
    [images,
    [tags,rating,date,keys],
    [len_comments,text,bestcomments]]
    """
    soup = bs(getpage(page).content, "html.parser")
    images = []
    temptext = []
    tempdate = []
    temprating = []
    tempkey = []
    temptags = []
    templencom = []
    tempbestcom = []
    # block selection
    for i in soup.select(".article.post-normal"):

        datatext = []
        # парс текста в посте если он имеется
        for io in i.select(".post_content > div"):
            temp = io.get_text(separator="\n")
            if temp:
                datatext.append(temp)

                # лучший коммент (если он есть) тексты + имя юзеров  и тд + прикрепленные пикчи и аватары
            tempbestcom.append(get_info(i, '.post_comment_list > div > div'))

        temptags.append(get_info(i, ".post_top > .taglist > b > a"))
        # рейтинг поста
        # temprating.append(info(i, ))
        # temp = []
        for ay in i.select(".ufoot > div > .post_rating > span"):
            # creating dict with tags
            try:
                temprating.append(float(ay.text))
            except ValueError as e:
                sys.stderr.write("<<!>>connect to VPN<<!>>\n")
                raise e

        # дата  день год месяц точное время
        tempdate.append(get_info(i, ".ufoot > div > .date > span > span"))

        # ссылка на пост
        for ay in i.select(".ufoot > div > .link_wr > a"):
            tempkey.append(os.path.basename(ay["href"]))

        for ay in i.select('.commentnum.toggleComments'):
            # creating dict with tags

            templencom.extend((re.findall(r'\d+', ay.text)))

        dataimage = []
        for i0 in i.select(".post_content"):
            for i1 in i0.select(".image"):
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
    return [images,
            [temptags, temprating, tempdate, tempkey],
            [templencom, temptext, tempbestcom]]


def get_val_by_index(value, index):
    """
    возвращает элементы по индексу

    :param value: элементы для сортировки
    :param index: индексы
    :return: сортированный массив
    """
    return np.array(value, dtype=object)[index]


@njit
def sort_by_rate_comments(val, rating=0):
    """
    Рейтинг = imfo[1] | Комменты - imfo[4]


    :param info: 1 аргумент переменная с информацией
    :param rating: 2 аргумент - цифра, ниже этого значения посты не пройдут
    :return: отсортированные индексы
    """
    ln = len(val)
    init_ind = np.empty(ln, dtype=np.uint)
    counter = 0
    for i in range(ln):
        if val[i] >= rating:
            init_ind[counter] = i
            counter += 1

    return init_ind[:counter]


def except_tag(info, tagexceptions: list, spike=None):
    """
    индекс тегов - info[0]

    :param info: принемает масив с информацией
    :param tagexceptions: список с исключениями которые вы выбераете например [фурри, furry]
    :param spike: по умолчанию если все теги присудствуют то пост будет считаться
    засчитаным, если же вы поставите 1 то достаточно будет одного тега для того что бы пост прошел
    :return: возвращает индексы
    """
    if spike is None:
        spike = len(tagexceptions)
    ln = len(info)

    counter = 0
    ind = np.empty(ln, dtype=np.uint)

    for i, v in enumerate(info):
        excepet_counter = 0
        for i0 in tagexceptions:
            if i0 in v:
                excepet_counter += 1

        if not excepet_counter >= spike:
            ind[counter] = i
            counter += 1

    return ind[:counter]


def sort_by_tag(info, tagexceptions: list, spike=None):
    """
    индекс тегов - info[0]

    :param info: принемает масив с информацией
    :param tagexceptions: список с исключениями которые вы выбераете например [хоба!, anime]
    :param spike: по умолчанию если все теги присудствуют то пост будет считаться
    засчитаным, если же вы поставите 1 то достаточно будет одного тега для того что бы пост прошел
    :return: возвращает новый отсортированный список

    """
    if spike is None:
        spike = len(tagexceptions)

    indexes = []

    for i, v in enumerate(info):
        counter = 0
        for i0 in tagexceptions:
            if i0 in v:
                counter = counter + 1
            if counter == spike:
                indexes.append(i)
                break
    return np.array(indexes)


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
        return None


def parse_user_tag_list(page: str, fullname=False):
    """
    парсит подписки (теги) юзера

    :param page: user page /user/username
    :param fullname: разрешить полные имена (отключает basename)
    :return: narray
    """
    temp = []
    if fullname:
        try:
            soup = bs(rq.get(page).content, "html.parser")
            for i in soup.select(".sidebar_block.blogs_wr > .sidebarContent"):
                for i0 in i.findAll(["a"]):
                    temp.append(urllib.parse.unquote(i0["href"]))
            return np.array(temp)
        except ConnectionError:
            print(messages[0])
            # sleep for a bit in case that helps
            # try again
            time.sleep(2)
            print(messages[2])
            return parse_user_tag_list(page, fullname)
    else:
        try:
            soup = bs(rq.get(page).content, "html.parser")
            for i in soup.select(".sidebar_block.blogs_wr > .sidebarContent"):
                for i0 in i.findAll(["a"]):
                    temp.append(os.path.basename(urllib.parse.unquote(i0["href"])))
            return np.array(temp)
        except ConnectionError:
            print(messages[0])
            # sleep for a bit in case that helps
            # try again
            time.sleep(2)
            print(messages[2])
            return parse_user_tag_list(page, fullname)


def download_images(images,multprocess_d = False, warn_on=True):
    """

    :param images: 1 аргумент принемает подготовленный список изображений (get_rdy(images) просто вставьте это)

    :param download_path: 2 аргумент в какую дирректорию надо скачивать

    :param warn_on: 3 аргумент отключения предупреждений по уполчанию влючено

    """
    foopoiner = mtdownloader
    if multprocess_d:
        foopoiner = mpdownloader
    
    # эта функция интуитивно понятна
    if warn_on:
        if len(images) == 0:
            print(messages[3])
        else:
            print("\n<<Download", len(images), "files?>>\n")
            x = input("><Proceed ([y]/n)?><")
            if x.lower() == "y":
                
                foopoiner(images)
            elif x.lower() == "n":
                print("<<exiting>>")
            else:
                print("><!Input value is incorrect, try again.!><\n[y - Yes]\n[n - No]")
                download_images(images)

    else:
        foopoiner(images)


def save_var_ovr(var, name="new_pkl_file"):
    """
    save variable with overwrite if name exists

    :param var: variable
    :param name: path/filename
    :return: pkl file (with overwrite if exists with same name)
    """
    with open(name + ".pkl", "wb") as f:
        pickle.dump(var, f)


def save_var(var, name="new_pkl_file", __=""):
    """
    save variable without overwrite

    :param var: variable
    :param name: path/filename
    :return: pkl file
    """
    if os.path.isfile(name + str(__) + ".pkl"):
        if __ == "":
            __ = "0"
        else:
            __ = int(__) + 1
        save_var(var, name, __)
    else:
        save_var_ovr(var, name + str(__))


def load_var(file):
    """
    load variable

    :param file: path/filename
    :return: var data
    """
    with open(file, "rb") as f:
        var = pickle.load(f)
    return var


def votegun(posts_array, cookie: str, token, vote=True, __abyss="0"):
    """
    плюсо/минусо-мет
    (просьба не злоупотреблять этой функцией)

    :param posts_array: номера постов(одномерный масив)
    :param cookie: куки(что бы их узнать зайдите на сайт и нажмите f12 -> network -> проголосуйте за любой пост -> в появившейся загрузке в пункте reqest headers будет ваша куки)
    :param token: все тоже самое что и с куки, в самом низу должен быть токен
    :param vote: голосует за или против(True/False)
    :param abyss: понятие не имею нужен он или нет(у меня он был 0)
    :return: void
    """
    if 'token=' in token:
        token.replace("token=", "")
    header = ({
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en,ru-RU;q=0.9,ru;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': None,
        'DNT': '1',
        'Host': 'joyreactor.cc',
        'Referer': 'http://joyreactor.cc/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    })
    header["Cookie"] = cookie

    if vote:
        votefor = "plus"
    else:
        votefor = "minus"
    for i in posts_array:
        adr = 'http://joyreactor.cc/post_vote/add/' + str(i) + '/' + votefor + '?token=' + token + '&abyss=' + __abyss
        rq.get(adr, headers=header)
        time.sleep(info_struct.timeout)


def parse_user_comments(userpage):
    pass


def get_popular_tags(t="s", till=101):
    """
    получить список самых популярных тегов


    :param t: s = от количества подписок на тег, r - от рейтинка (низходящий)
    :param till: до какой страницы сканировать (максимум 101)
    :return: [имена, количество постов в теге, количество подписок, рейтинг тега, ссылка на иконку тега] narray object
    """

    if t[0] == "s":
        tmptype = "subscribers/"
    elif t[0] == "r":
        tmptype = ""
    else:
        raise TypeError

    tmpicon = []
    tmpname = []
    tmptagrate = []
    tmpsub = []
    tmp_p_count = []

    for i in range(2, till):  # 101
        soup = bs(getpage("http://joyreactor.cc/tags/" + tmptype + str(i)).content, "html.parser")
        for itag in soup.findAll("div", {"class": "blog_list_item"}):

            for ii in itag.select(".blog_list_avatar > a > img"):
                tmpicon.append(ii["src"])

            rc = itag.select(".blog_list_name > small")
            tmpsub.extend(re.findall(r'\d+', rc[1].text))

            tmp = re.findall(r'\d+', rc[0].text)
            tmp.insert(-1, ".")
            tmptagrate.append("".join(tmp))

            ap = itag.select(".blog_list_name > strong > a")
            for iiii in ap:
                tmpname.append(iiii["title"])

            posts_c = str(ap[0])
            x = len(posts_c)
            for count in range(x - 5, 0, -1):
                if posts_c[count] == "(":
                    try:
                        x = posts_c[count + 1:-5]
                        tmp_p_count.append(int(x))
                    except ValueError:
                        tmp_p_count.append(0)
                    break
        time.sleep(info_struct.timeout)
    return np.array([tmpname,
                     np.array(tmp_p_count, dtype=np.int),
                     np.array(tmpsub, dtype=np.int),
                     np.array(tmptagrate, dtype=np.float),
                     tmpicon], dtype=object)


__author__ = "ExE"
__version__ = "0.1.9"
# Я реакторе - FEAR2k


# legacy

#
# def sort_by_rate_comments(linksbase, info_index, rating=0):
#     """
#     Рейтинг = imfo[1] | Комменты - imfo[4]
#
#
#     :param linksbase: 1 аргумент это что надо отсартировать картинки/текст
#     :param info: 2 аргумент переменная с информацией
#     :param rating: 3 аргумент - цифра, ниже этого значения посты не пройдут
#     :return: список с удаленными в них постами ниже определенного рейтинга
#     """
#
#     sorted_links = []
#     idexes = np.argsort(info_index)[::-1]
#     for i, v in enumerate(araara(info_index)[idexes]):
#         if v < rating:
#             break
#         sorted_links.append(linksbase[idexes[i]])
#
#     return sorted_links

#
# def sort_by_tag(linkbase=list, info=list, tagexceptions=list, spike=None):
#     """
#
#     :param linkbase: принемает многомрный список изображений/текста
#     :param info: принемает масив с информацией
#     :param tagexceptions: список с исключениями которые вы выбераете например [фурри, furry]
#     :param spike: по умолчанию если все теш=ги присудствуют то пост будет считаться
#     засчитаным, если же вы поставите 1 то достаточно будет одного тега для того что бы пост прошел
#     :return: возвращает новый отсортированный список
#
#     """
#     if spike is None:
#         spike = len(tagexceptions)
#
#     sortedlist = []
#
#     for i, v in enumerate(info):
#         counter = 0
#         for i0 in tagexceptions:
#             if i0 in v:
#                 counter = counter + 1
#             if counter == spike:
#                 sortedlist.append(linkbase[i])
#                 break
#     return sortedlist

#
# def except_tag(linkbase=list, info=list, tagexceptions=list, spike=None):
#     """
#
#     :param linkbase: принемает многомрный список изображений/текста
#     :param info: принемает масив с информацией
#     :param tagexceptions: список с исключениями которые вы выбераете например [фурри, furry]
#     :param spike: по умолчанию если все теш=ги присудствуют то пост будет считаться
#     засчитаным, если же вы поставите 1 то достаточно будет одного тега для того что бы пост прошел
#     :return: возвращает новый отсортированный список
#     """
#     if spike is None:
#         spike = len(tagexceptions)
#
#     sortedlist = []
#     print(len(linkbase),len(info))
#     for i, v in enumerate(info):
#         counter = 0
#         for i0 in tagexceptions:
#             if i0 in v:
#                 counter = counter + 1
#         if not counter >= spike:
#             sortedlist.append(linkbase[i])
#
#     return sortedlist
#
