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


def is_file(filename):
	while not os.path.exists(filename):
		global toaster
		toaster.show_toast("Pozor!", "Súbor neexistuje.")
		return None
	return filename


def load_from_file(p_filename, p_arr):
	for line in open(p_filename, "r"):
		processed = line.split(' ')
		p_arr.append(Link(processed[0], int(processed[1]), int(processed[2]), processed[3], processed[4]))


toaster = ToastNotifier()
array = []
file = is_file("links")
if file is not None:
	load_from_file(file, array)
	browser_link = browser_link + " %s"
	while True:
                toaster.show_toast("Začiatok", "Fungujem.",)
		now = datetime.datetime.now()
		for x in array:
			if (now.strftime("%A") == x.day) and (now.hour == x.hour) and (now.minute == x.minute):
				webbrowser.get(browser_link).open(x.link_to)
				toaster.show_toast(x.title, "Sústreď sa.",)
		sleep(59)
