import pickle
import os
import requests as req
import time

# Saving the objects:
sorted_links = ([])
links = []
d_path = r"E:\parser_data"

# Getting back the objects:
with open('ecchi(4979-1)info.pkl', "rb") as f:  # Python 3: open(..., 'rb')
    inf = pickle.load(f)
with open('ecchi(4979-1)pic.pkl', "rb") as f:  # Python 3: open(..., 'rb')
    linksbase = pickle.load(f)

##################
ratingf = 1  # включение-1 выключение-0 функции сортировки по рейтингу поста infof тоже должна быть включена
rating = 60  # все посты выше этого значения будут скачены

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
#   return list(dict.fromkeys(x))

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


        def getimage(Im_link, request, path_FileBaseName):
            try:
                time.sleep(2)  # don't touch it coz ping need to not overload website or get frecking ban
                # не трогать задержка нужна что бы не перегружать вэбсайт и не получить ебаный бан от сайта
                with open(path_FileBaseName, 'wb') as f:  # открываем файл
                    f.write(req.get(Im_link, headers=request).content)
                      # делаем запрос на получение файла

            except Exception:
                print(
                    "упс, похоже что то произошло интернетом, пожалуста проверьте соединение и "
                    "переподключитесь к впн")
                # sleep for a bit in case that helps
                input("для переподключения введите все что угодно:")
                # try again
                return getimage(Im_link, request, path_FileBaseName)

        for Im_link in links:  # итерация хуяция

            print("files left:", counter)
            counter = counter - 1


            path_FileBaseName = d_path + os.sep + os.path.basename(Im_link)
            # проверяем существует ли файл в диооектории

            if not os.path.exists(path_FileBaseName):

                getimage(Im_link, request, path_FileBaseName)
            else:
                print("Файл",os.path.basename(Im_link),"уже существует в директории ("+d_path+")")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print("\n\n#===================================#\n# Code sequence successful complete #"
      "\n#===================================#")



__version__ = "0.1"
__author__ = "ExE https://github.com/ExecutorExe"