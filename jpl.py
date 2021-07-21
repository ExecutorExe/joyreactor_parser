# "Conda_env_3.7"
import os
import os.path
import sys
import urllib.parse
import requests as rq  # '2.24.0'
from bs4 import BeautifulSoup as bs  # version '4.9.1'
import numpy as np  # 1.19.1
from multiprocessing import cpu_count  # GIL is shit
from concurrent.futures import ThreadPoolExecutor
import time
import datetime

# си подобные структы
class info_struct:
    thread_num = cpu_count()
    timeout = 1
    d_path = os.path.join(os.path.expanduser("~"), "Downloads")
    cookie = ""
    #:param cookie: куки(что бы их узнать зайдите на сайт и нажмите f1
    # -> network -> проголосуйте за любой пост -> в появившейся загрузке
    # в пункте reqest headers будет ваша куки)

class PidorError:
    """
    Pidori pamagite
    """
def getelmlist(i, path):
    temp = []
    for ay in i.select(path):
        temp.append(ay.text)

    return temp


class datastruct:
    def __init__(self,
                 images: list,
                 text: str,
                 tags: list,
                 rating: float,
                 datetime: float,
                 comments_len: int
                 ):
        self.images = images
        self.text = text
        self.tags = tags
        self.rating = rating
        self.datetime = datetime
        self.comments_len = comments_len


def mtdownloader(links):
    """
    single (master) thread donwnloader
    """
    for i in links:
        getimage(i)


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
    except ValueError as e:
        if "/post/" in page or "/tag/" in page or "/user/" in page or "/search/" in page:
            return 1
        else:
            raise e


def mpdownloader(links):
    """
    create N workers(processes) for function
    # why i can't just
    # #pragma omp parallel for shared(links) schedule(dynamic)
    # in python """
    with ThreadPoolExecutor(max_workers=info_struct.thread_num) as p:
        p.map(getimage, links)


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
    request["Host"] = Im_link[7:Im_link.index('.', 7)] + ".joyreactor.cc"
    # print(request["Host"],Im_link)
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



def mparser(link:str,fromto:list):
    """
    m reactor parsear 
    link - example: http://m.reactor.cc/tag/echi
    fromto - examle [10,0]
    
    return lists images,tags,rating
    """
    mi = []
    mt = []
    mr = []
    h = {
    "Host": "m.reactor.cc",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Cookie": "",
    "Upgrade-Insecure-Requests": '1',}
    h["Cookie"] = info_struct.cookie

    for n in range(fromto[0],fromto[1],-1):

        soup = bs(rq.get(link + "/" + str(n),headers=h).content, "html.parser")
        soup = soup.select(".postContainer")
        if not soup:
            return -1
    
        for i in soup:
            img = []
            title = []
            r = np.float32((i.find_all("span",class_="post_rating"))[0].text[10:])
            for iii in i.select(".taglist")[0].find_all("a"):
                title.append(iii["title"])
            for ii in i.find_all("img"):
                img.append(urllib.parse.unquote(ii["src"]).replace("post/","post/full/",1))
            mi.append(img)
            mt.append(title)
            mr.append(r)
    return mi,mt,mr


def try_mreactor(num:str):
    h = {
    "Host": "m.reactor.cc",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Cookie": "",
    "Upgrade-Insecure-Requests": '1',}
    h["Cookie"] = info_struct.cookie
    l = "http://m.reactor.cc"
    soup = bs(rq.get(l + "/post/" + num,headers=h).content, "html.parser")
    soup = soup.select(".image")
    if not soup:
        return 0
    for i in soup:
        img = []
        for ii in i.find_all("img"):
            img.append(urllib.parse.unquote(ii["src"]).replace("post/","post/full/",1))
    return img

def parse_page(link: str, base: dict):
    """
    Parse single page
    :param link: pagename example: http://reactor.cc
    :param base: dict
    :param updf: return non zero value if hash are exits in hashtable


    :return: 
    | returns 0 if all posts are scanned  |
    | positive if some posts are exists   |
    | negative if errors                  |
    | -1 if can't find any posts          |
    """


    exitvalue = np.int8(0)
    soup = bs(rq.get(link).content, "html.parser")
    # block selection
    soup = soup.select(".article.post-normal")
    if not soup:
        print("404")
        return -1
    for i in soup:
        # key
        head = os.path.basename(i.select(".ufoot > div > .link_wr > a")[0]["href"])


        txt = ""
        # парс текста в посте если он имеется
        for tx in i.select(".post_content > div"):
            txt = tx.get_text(separator="\n")

                

        listtags = getelmlist(i, ".post_top > .taglist > b > a")
        # рейтинг поста
        txtrate = i.select(".ufoot > div > .post_rating > span")[0].text
        try:
            r = np.float32(txtrate)
        except ValueError as e:
            sys.stderr.write("<<!>>connect to VPN<<!>>\n")
            raise e

        # дата  день год месяц точное время
        tm = i.select(".ufoot > div > .date > span > span")
        # перевод в сырой вид
        tm = time.mktime(datetime.datetime.strptime(tm[0].text + '.' + tm[1].text, \
                                                    "%d.%m.%Y.%H:%M").timetuple())
        # len comments
        lc = np.uint32((i.select('.commentnum.toggleComments')[0].text)[12:])
        dataimage = []
        if not i.find('img', alt="Copywrite"):
            
            for i1 in i.select(".post_content")[0].select(".image"):
                # "a" - большие изображения которые надо разворачивать + гифки
                # "img" - мелкие изображения которые слишком малы что бы разворачивать
                for i2 in i1.findAll(["a", "img"]):
                    # парс исзображения
                    if i2.has_attr("href") and i2.get("class")[0] == "prettyPhotoLink":
                        # decode urlencoded and add to list
                        dataimage.append(urllib.parse.unquote(i2["href"]))
                        break  # coz big siz imaga have dub of small
                    else:
                        # если нет достаточно крупного изображения
                        if i2.has_attr("src"):
                            dataimage.append(urllib.parse.unquote(i2["src"]))
        else:
            try:
                kkkkk = try_mreactor(head)
                if 0 != kkkkk:
                    dataimage = kkkkk
                else:
                    sys.stderr.write("mreactor exception, post: %s\nset cookies in info_struct\nif this not helps check request header in jpl.py->try_mreactor->h" % head)
                    continue
            except Exception as e:
                sys.stderr.write("Pidor Error:\nPost " + head + " can't be saved because of Copywrite\n")
                exitvalue |= np.int8(0b10000000)
                sys.stderr.write("mreactor exception, post: %s\n" % head)
                sys.stderr.write(str(e))
                continue
        
        p = datastruct(dataimage, txt, listtags, r, tm, lc)
        if not head in base:
            base[head] = p

    return exitvalue
