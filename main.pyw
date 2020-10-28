import os
import webbrowser
from time import sleep
from win10toast import ToastNotifier
import datetime

browser_link = "C:/Users/matej/AppData/Local/Programs/Opera GX/launcher.exe"


class Link:
    def __init__(self, day, hour, minute, title, link_to):
        self.day = day
        self.hour = hour
        self.minute = minute
        self.title = title
        self.link_to = link_to


def file_exists(p_file_name):
    while not os.path.exists(p_file_name):
        global toaster
        toaster.show_toast("Pozor!", "Súbor neexistuje.")
        return None
    return p_file_name


def load_from_file(p_file_name, p_arr):
    for line in open(p_file_name, "r"):
        separated_line = line.split(' ')
        p_arr.append(Link(separated_line[0], int(separated_line[1]),
                          int(separated_line[2]), separated_line[3], separated_line[4]))


toaster = ToastNotifier()
array = []
file = file_exists("links")
if file is not None:
    before_change = os.stat(file).st_mtime
    load_from_file(file, array)
    browser_link = browser_link + " %s"
    toaster.show_toast("Začiatok", "Fungujem.")
    while True:
        now = datetime.datetime.now()

        if before_change != os.stat(file).st_mtime:
            before_change = os.stat(file).st_mtime
            load_from_file(file, array)

        for x in array:
            if (now.strftime("%A") == x.day) and (now.hour == x.hour) and (now.minute == x.minute):
                webbrowser.get(browser_link).open(x.link_to)
                toaster.show_toast(x.title, "Sústreď sa.")
                sleep(60)
        sleep(10)
