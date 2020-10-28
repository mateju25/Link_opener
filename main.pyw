import os
import webbrowser
from time import sleep
from win10toast import ToastNotifier
import datetime


class Link:
    def __init__(self, line):
        self.day = line[0]
        self.hour = int(line[1])
        self.minute = int(line[2])
        self.title = line[3]
        self.browser = line[4]
        self.link_to = line[5]


class Browser:
    def __init__(self, line):
        self.browser = line[0]
        self.link_to = line[1] + " %s"


class File:
    def __init__(self, file_name):
        self.file_name = file_exists(file_name)
        if self.file_name is None:
            return
        self.modif_time = os.stat(file_name).st_mtime
        self.array_of_items = []

    def load_new_items(self):
        load_from_file(self.file_name, self.array_of_items)

    def is_modified(self):
        if self.modif_time != os.stat(self.file_name).st_mtime:
            global toaster
            toaster.show_toast("Upozornenie!", "Zmena vstupneho suboru.")
            self.modif_time = os.stat(self.file_name).st_mtime
            self.load_new_items()


def file_exists(p_file_name):
    while not os.path.exists(p_file_name):
        global toaster
        toaster.show_toast("Pozor!", "Súbor neexistuje.")
        return None
    return p_file_name


def load_from_file(p_file_name, p_arr):
    for line in open(p_file_name, "r"):
        line = line.split('\n')[0]
        if p_file_name == 'browsers':
            separated_line = line.split(' ', 1)
            p_arr.append(Browser(separated_line))
        elif p_file_name == 'links':
            separated_line = line.split(' ')
            p_arr.append(Link(separated_line))


toaster = ToastNotifier()

links_file = File("links")
browser_file = File("browsers")

if (links_file.file_name is not None) and (browser_file.file_name is not None):

    links_file.load_new_items()
    browser_file.load_new_items()

    toaster.show_toast("Začiatok", "Fungujem.")
    while True:
        now = datetime.datetime.now()

        links_file.is_modified()
        browser_file.is_modified()

        for link_item in links_file.array_of_items:
            if (now.strftime("%A") == link_item.day) and (now.hour == link_item.hour) and (now.minute == link_item.minute):

                for browser_item in browser_file.array_of_items:
                    if browser_item.browser == link_item.browser:
                        webbrowser.get(browser_item.link_to).open(link_item.link_to)

                toaster.show_toast(link_item.title, "Sústreď sa.")
                sleep(60)
        sleep(10)
