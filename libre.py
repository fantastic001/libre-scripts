# coding=UTF-8

from dokuwiki.parsers import Parser, LineParser
from dokuwiki.elements import LineElement
from dokuwiki.dokuwikixmlrpc import DokuWikiClient 
from dokuwiki.html import html_encode

import re

class LibreTextParser(Parser): 
	def onDocumentStart(self): 
		self.output = "<body>\n"
		self.libre_title = ""
		self.libre_author = ""
		self.libre_status = "U_PRIPREMI"
	def onHeading(self, level, text):
		self.output += "<h" + str(7 - level) + ">" + text + "</h" + str(7 - level) + ">\n"
		if level == 6: 
			self.libre_title = text.strip()
	def onListStart(self, mode): 
		self.output += "<ul>\n"
	def onListEnd(self): 
		self.output += "</ul\n>"
	def onListItem(self, level, text): 
		self.output += "<li>" + text + "</li>\n"
	def onCodeStart(self, language, filename): 
		self.output += "<pre>\n"
	def onCode(self, text): 
		self.output += text + "\n"
	def onCodeEnd(self): 
		self.output += "</pre>\n"
	def onParagraphStart(self): 
		self.output += "<p>"
	def onParagraphEnd(self): 
		self.output += "</p>\n"
	def onText(self, text):
		
		# do some libre-specific stuff 
		if text.strip() in ["U_PRIPREMI", "ORIGINAL", "PRIHVACEN", "LEKTORISAN", "PROVEREN"]:
			self.libre_status = text.strip()
			return 
		m = re.compile(r"(Autor|autor|autori|Autori|Аутор):? *(.*)") # check for author matching 
		match = m.match(text) 
		if match: 
			self.libre_author = match.group(2)

		bold = False
		italic = False
		underline = False

		t = html_encode(text) # encode text for HTML 
		l = LineParser()
		t = l.prepare(t) 
		for e in l.parse(t): 
			element = LineElement(e) 
			if element.getMode() == LineElement.Mode.NORMAL: 
				self.output += e 
			elif element.getMode() == LineElement.Mode.ITALIC and not italic: 
				italic = True
				self.output += "<i>"
			elif element.getMode() == LineElement.Mode.ITALIC and italic: 
				self.output += "</i>"
				italic = False 
			elif element.getMode() == LineElement.Mode.BOLD and not bold: 
				bold = True
				self.output += "<strong>"
			elif element.getMode() == LineElement.Mode.BOLD and bold:
				self.output += "</strong>"
				bold = False 
			elif element.getMode() == LineElement.Mode.UNDERLINE and not underline: 
				underline = True
				self.output += "<u>"
			elif element.getMode() == LineElement.Mode.UNDERLINE and underline: 
				self.output += "</u>"
	
	def onDocumentEnd(self): 
		self.output += "</body></html>"
	
	def getOutput(self, stylesheet=None): 
		head = "<html>\n<head>\n<title>WIKI Page</title>\n"
		head+= '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n'
		if stylesheet != None: 
			head += "<style type='text/css'>\n" + stylesheet + "\n</style>\n"
		head += "</head>\n"
		return head + self.output

class LibreText(object): 
	
	def __init__(self, text): 
		
		parser = LibreTextParser() 
		blocks = text.split("\n")
		for line in blocks: 
			parser.parse(line) 
		parser.finish()
		
		self.title = parser.libre_title 
		self.author = parser.libre_author 
		self.status = parser.libre_status
		self.html = parser.getOutput()
		self.text = text 

	def isChecked(self): 
		"""
		Checks whether text has a status PROVEREN 
		"""
		return self.status == "PROVEREN"

	def getTitle(self): 
		"""
		Returns text title
		"""
		return self.title 
	
	def getText(self): 
		"""
		Returns text
		"""
		return self.text 

	def getAuthor(self): 
		"""
		Returns author information
		"""
		return self.author
	def getStatusString(self): 
		"""
		Returns status as a string representation
		"""
		return self.status 
	def getHTML(self): 
		"""
		Returns HTML of a text
		"""
		return self.html


class LibreManager(object): 
	
	def __init__(self, username, password): 
		self.remote = DokuWikiClient("https://libre.lugons.org/wiki", username, password)

	def getPage(self, page): 
		"""
		Returns specified page id as a LibreText object

		NOTE: page should be with namespace
		"""
		return LibreText(self.remote.page(page))
	
	def getAllLinked(self, source): 
		"""
		Returns a list of LibreText objects which are all pages linked from specified page
		"""
		res = []
		links = self.remote.links(source) 
		for link in links: 
			if link["type"] == "local": 
				print link["page"]
				libretext = self.getPage("wiki:" + link["page"])
				print "Title: " + libretext.getTitle()
				res.append(libretext)
		return res


