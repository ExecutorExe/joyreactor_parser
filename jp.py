# Тут находятся более хайлевловые функции
import re
import pickle
import sys

from .jpl import *
from requests.exceptions import ConnectionError

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
messages = np.array(["<<!alert, connection error!>>",
                     "><to reconnect type anything><",
                     "<<trying to reconnect>>",
                     "<<files does not found>>"])

# DRY -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#-
cerrortimeout = 5  # if connection error


def uni(array, leng, empty_array):
    """
    unique with order
    empty_array[:count]
    :param array: array to unique
    :param leng: len
    :param empty_array: np.empty(len(arr),dtype=np.uint)
    :return: size_t
    Я хоть и не частро использую goto в C, но в этом коде она бы зашла на много лучше
    Пример:
    //Но читабельность отвратительна
    size_t uni(int* restrict arr,size_t* restrict arr_i, size_t* restrict size){
        size_t i = 0;
        size_t ii;
        size_t count = 0;
        goto A;
        A:
            ii = 0;
            if (*size > i)
                goto B;

            return count;
        B:
            
            if (ii < count){
                if(arr[i] == arr[arr_i[ii++]]){
                    i++;
                    goto A;
                }
                goto B;
            }
            
            arr_i[count++] = i++;
            goto A;
}
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


def getpage(page):
    try:
        # getting url
        url = rq.get(page)
        return url
    except ConnectionError:
        sys.stderr.write(messages[0])
        input(messages[1])

        # try again
        return getpage(page)


def to_ndarray(base: dict):
    """
    convert base to ndarray
    :param base: dict
    :return: [
    images,
    txt,
    tags,
    rating,
    date,
    keys,
    len_comments] dtype = object
    """
    images_ = list()
    tags_ = list()
    rating_ = list()
    date = list()
    lencomments = list()
    txt = list()
    keys_ = list()
    for i in base.keys():
        images_.append(base[i].images)
        txt.append(base[i].text)
        tags_.append(base[i].tags)
        rating_.append(base[i].rating)
        date.append(base[i].datetime)
        lencomments.append(base[i].comments_len)
        keys_.append(i)
    return \
           [np.array(images_, dtype=object),
                    np.array(txt, dtype=object),
                    np.array(tags_, dtype=object),
                    np.array(rating_, dtype=np.float32),
                    np.array(date, dtype=np.float64),
                    np.array(keys_).astype(np.uint32),
                    np.array(lencomments, dtype=np.uint32)]
                


# END_DRY -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#- -#-


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


def parser2(page: str, from_page : int, until_page=0, upd=None,dct = False,eignore = True):
    """
    парсер может сканировать теги or основные страницы по типу best or юзеров одиночные посты

    - upd: dict | update existing data

    -dct: bool | return dict

    Output:
    -------
    [images,text,tags,rating,date,keys,len_comments] dtype=object
    """
    m = np.int8(0xFF)
    if eignore:
        m = np.int8(0b01111111)
    if page[-1] == "/":
        page = page[:-1]

    base = dict()
    if upd == dict:
        base = upd

    while not from_page == until_page:

        try:
            sys.stdout.write("left: " + str(from_page) + "\0\r")
            q = parse_page(page + "/" + str(from_page), base)

                
            q &= m
            if 0 > q:
                sys.stderr.write("Exit value: " + str(q))
                raise Exception

            
            if q > 0 and upd:
                break
            from_page -= 1
            time.sleep(info_struct.timeout)

        except (ConnectionError, ValueError):
            input("input anything to reconnect\n\r")
            continue
    sys.stdout.write("\n")
    if dct:
        return base
    else:
        return to_ndarray(base)


def get_val_by_index(value, index):
    """
    возвращает элементы по индексу

    :param value: элементы для сортировки
    :param index: индексы
    :return: сортированный массив
    """
    return np.array(value, dtype=object)[index]


def filter_by_intorfloat(val, rating=0):
    """
    Рейтинг = imfo| Комменты - imfo


    :param info: аргумент переменная с информацией
    :param rating: аргумент - цифра, ниже этого значения посты не пройдут
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


def filter_by_tag(info, tagexceptions: list, spike=None):
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


def download_images(images, multprocess_d=False, warn_on=True):
    """

    :param images: 1 аргумент принимает подготовленный список изображений get_rdy(images)

    :param multprocess_d: 2 аргумент включает multiprocess download (выключено по умолчанию)

    :param warn_on: 3 аргумент отключения предупреждений по умолчанию влючено

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
            x = input("><Proceed (y/n)?><")
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


def votegun(posts_array, token, vote=True, __abyss="0"):
    """
    плюсо/минусо-мет
    (просьба не злоупотреблять этой функцией)

    :param posts_array: номера постов(одномерный масив)
    :param token: все тоже самое что и с куки, в самом низу должен быть токен
    :param vote: голосует за или против(True/False)
    :param abyss: понятие не имею нужен он или нет(у меня он был 0)
    :global info_struct param cookie: куки(что бы их узнать зайдите на сайт и нажмите f12 -> network -> проголосуйте за любой пост -> в появившейся загрузке в пункте reqest headers будет ваша куки)

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
    header["Cookie"] = info_struct.cookie

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
