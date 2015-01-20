# -*- coding: utf-8 -*- 

# This script generates news page for LiBRE! magazine 
# It i in the following format 
# 
# ====== LiBRE! vesti ${issue} ======
# 
# //**Title**//\\
# $day. $month $year.
# 
# $description
# 
# Koristan link: $url \\
# \\
# 
# //**$title**//\\
# $day. $month, $year.
# 
# $description
# 
# Koristan link: $url \\
# \\ 
# 
# ... 
# ~~DISCUSSION~~
# 

from dokuwiki.parsers import LineParser

from datetime import date 

cir_lat_map = {
	"љ": "lj", 
	"њ": "nj", 
	"е": "e", 
	"р": "r", 
	"т": "t", 
	"з": "z",
	"у": "u", 
	"и": "i", 
	"о": "o", 
	"п": "p", 
	"а": "a",
	"с": "s", 
	"д": "d", 
	"ф": "f", 
	"г": "g", 
	"х": "h", 
	"ј": "j", 
	"к": "k", 
	"л": "l", 
	"џ": "dž", 
	"ц": "c", 
	"в": "v", 
	"б": "b", 
	"н": "n", 
	"м": "m", 
	"ш": "š", 
	"ђ": "đ",
	"ж": "ž", 
	"ч": "č", 
	"ћ": "ć", 
	"Љ": "Lj",
	"Њ": "Nj",
	"Е": "E", 
	"Р": "R",
	"Т": "T", 
	"З": "Z", 
	"У": "U",
	"И": "I", 
	"О": "O",
	"П": "P",
	"А": "A",
	"С": "S", 
	"Д": "D", 
	"Ф": "F", 
	"Г": "G", 
	"Х": "H", 
	"Ј": "J", 
	"К": "K", 
	"Л": "L", 
	"Џ": "Dž", 
	"Ц": "C", 
	"В": "V", 
	"Б": "B", 
	"Н": "N", 
	"М": "M", 
	"Ш": "Š", 
	"Ђ": "Đ", 
	"Ж": "Ž",
	"Ч": "Č",
	"Ћ": "Ć"
}


def lat_to_cir(text):
    ntext = ""
    ntext = text
    #print "# Translate 2-letter letters first"
    # Translate 2-letter letters first 
    for cl in list(cir_lat_map.keys()): 
    	if len(cir_lat_map[cl]) == 2: 
    		#print cir_lat_map[cl] + " -> " + cl
    		ntext = ntext.replace(cir_lat_map[cl], cl)
    
    
    #print "# Translate 1-letter letters"
    # Translate 1-letter letters
    for cl in list(cir_lat_map.keys()): 
    	if len(cir_lat_map[cl]) == 1: 
    		#print cir_lat_map[cl] + " -> " + cl
    		ntext = ntext.replace(cir_lat_map[cl], cl)
    return ntext

class NewsTranslatorLineParser(LineParser): 
	def onStart(self): 
		self.output = ""
		self.translate = True
	def onNormal(self, text): 
		if self.translate: 
			self.output += lat_to_cir(text)
		else:	
			self.output += text
	def onItalicStart(self): 
		self.translate = False
	def onItalicEnd(self): 
		self.translate = True 
	def onBoldStart(self): 
		self.output += "**"
	def onBoldEnd(self): 
		self.output += "**"
	def onUnderlineStart(self):
		self.output += "__"
	def onUnderlineEnd(self):
		self.output += "__"
	def onLink(self, url, title): 
		self.output += "[[" + title + "|" + url + "]]"
	def onImage(self, params):
		self.output += "{{" + params + "}}"
	def getOutput(self): 
		return self.output 



def date_libre_format(d): 
	serbian_months = ["januar", "februar", "mart", "april", "maj", "jun", "jul", "avgust", "septembar", "oktobar", "novembar", "decembar"]

	day = str(d.day)
	month = serbian_months[d.month]
	year = str(d.year)
	return (day, month, year)


class LibreNewsItem(object):
	
	def __init__(self, _title, _date, _description, _url): 
		self.title = NewsTranslatorLineParser(_title).getOutput()
		#self.date = "%s. %s %s." % date_libre_format(_date)
		self.date = lat_to_cir(_date)
		self.description = NewsTranslatorLineParser(_description).getOutput()
		self.url = _url
			
	def __str__(self): 
		s = ""
		s += "//** %s **//\\\\\n" % self.title
		s += "%s\\\\\n" % self.date
		s += "%s\n" % self.description
		s += "\n"
		s += lat_to_cir("Koristan link: ") + self.url + " \\\\\n"
		s += "\\\\\n"
		s += "\n" 
		return s

print("Welcome to LiBRE! news generator!")
print("") 
issue = input("Enter issue number: ")
news = []
while True: 
	
	print("Enter q for quit and saving and viewing resulting page.") 
	print("Enter a to add new item.")
	# TODO Make it to work with python 3.x too 
	q = input("> ") 
	if q == "a":
		_title = input("Title: ")
		_date = input("Date (%d. %month %Y. format): ")
		_description = input("Description: ")
		_url = input("URL: ")
		news.append(LibreNewsItem(_title, _date, _description, _url))
	elif q == "q": 
		break 
	else: 
		print("Wrong command.") 
		continue


print("ORIGINAL") 

print(lat_to_cir("======LiBRE! vesti %s======" % str(issue)))
for item in news: 
	print(str(item))

print("") 
print("~~DISCUSSION~~")
