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
	u"љ": u"lj", 
	u"њ": u"nj", 
	u"е": u"e", 
	u"р": u"r", 
	u"т": u"t", 
	u"з": u"z",
	u"у": u"u", 
	u"и": u"i", 
	u"о": u"o", 
	u"п": u"p", 
	u"а": u"a",
	u"с": u"s", 
	u"д": u"d", 
	u"ф": u"f", 
	u"г": u"g", 
	u"х": u"h", 
	u"ј": u"j", 
	u"к": u"k", 
	u"л": u"l", 
	u"џ": u"dž", 
	u"ц": u"c", 
	u"в": u"v", 
	u"б": u"b", 
	u"н": u"n", 
	u"м": u"m", 
	u"ш": u"š", 
	u"ђ": u"đ",
	u"ж": u"ž", 
	u"ч": u"č", 
	u"ћ": u"ć", 
	u"Љ": u"Lj",
	u"Њ": u"Nj",
	u"Е": u"E", 
	u"Р": u"R",
	u"Т": u"T", 
	u"З": u"Z", 
	u"У": u"U",
	u"И": u"I", 
	u"О": u"O",
	u"П": u"P",
	u"А": u"A",
	u"С": u"S", 
	u"Д": u"D", 
	u"Ф": u"F", 
	u"Г": u"G", 
	u"Х": u"H", 
	u"Ј": u"J", 
	u"К": u"K", 
	u"Л": u"L", 
	u"Џ": u"Dž", 
	u"Ц": u"C", 
	u"В": u"V", 
	u"Б": u"B", 
	u"Н": u"N", 
	u"М": u"M", 
	u"Ш": u"Š", 
	u"Ђ": u"Đ", 
	u"Ж": u"Ž",
	u"Ч": u"Č",
	u"Ћ": u"Ć"
}


def lat_to_cir(text):
    ntext = ""
    ntext = text
    #print "# Translate 2-letter letters first"
    # Translate 2-letter letters first 
    for cl in cir_lat_map.keys(): 
    	if len(cir_lat_map[cl]) == 2: 
    		#print cir_lat_map[cl] + " -> " + cl
    		ntext = ntext.replace(cir_lat_map[cl], cl)
    
    
    #print "# Translate 1-letter letters"
    # Translate 1-letter letters
    for cl in cir_lat_map.keys(): 
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
		s += "Koristan link: %s \\\\\n" % self.url
		s += "\\\\\n"
		s += "\n" 
		return s.encode("utf8")

print "Welcome to LiBRE! news generator!"
print 
issue = raw_input("Enter issue number: ")
news = []
while True: 
	
	print "Enter q for quit and saving and viewing resulting page." 
	print "Enter a to add new item."
	# TODO Make it to work with python 3.x too 
	q = raw_input("> ") 
	if q == "a":
		_title = raw_input("Title: ").decode("utf8") 
		_date = raw_input("Date (%d. %month %Y. format): ").decode("utf8")
		_description = raw_input("Description: ").decode("utf8")
		_url = raw_input("URL: ").decode("utf8")
		news.append(LibreNewsItem(_title, _date, _description, _url))
	elif q == "q": 
		break 
	else: 
		print "Wrong command." 
		continue


print "ORIGINAL" 

print lat_to_cir("======LiBRE! vesti %s======" % issue).encode("utf8")
print 
for item in news: 
	print str(item)

print 
print "~DISCUSSION~~"
