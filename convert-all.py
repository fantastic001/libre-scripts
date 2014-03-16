#!/usr/bin/python2

from PIL import Image
import os 
import string
import sys

def main():
	opts = {}
	opts["location"] = "/data/images"
	opts["quality"] = 50

	_q = False
	_l = False
	for arg in sys.argv: 
		if arg == "--quality": 
			_q = True
			continue
		if arg == "--location": 
			_l = True
			continue

		if _q: 
			try: 
				opts["quality"] = int(arg)
			except ValueError: 
				print "Please specify number for quality"
				exit(1)
			_q = False 
		if _l: 
			opts["location"] = arg
			_l = False
	
	location = opts["location"]

	### PDF
	
	print """
	
	Welcome to LiBRE script additionals by Stefan Nozinic (stefan <AT> lugons <DOT> org)
	
	"""
	
	print ">> Converting images for PDF..."
	print "..............................."

	if not os.path.exists(location + "/output"): 
		os.mkdir(location + "/output") 
	
	for image in os.listdir(location): 
		if os.path.isdir(location + "/" + image): 
			continue
		
		newname , ext = os.path.splitext(image)
		if ext == ".jpg" or ext == ".JPG" or ext == ".png" or ext == ".PNG" or ext == ".JPEG" or ext == ".gif" or ext == ".GIF":
			print "Image: " + image
			im = Image.open(location + "/" + image)	
			w , h = im.size
			nim = im.resize((898, (898*h)/w))	
			nim.save(location + "/output/" + newname + ".png", dpi=(300,300))
	
	### ePUB
	
	print ">> Converting images for ePUB..."
	print "................................"
	
	if not os.path.exists(location + "/output-epub"): 
		os.mkdir(location + "/output-epub") 
	
	for image in os.listdir(location): 
		if os.path.isdir(location + "/" + image): 
			continue
		newname , ext = os.path.splitext(image) 
		if ext == ".jpg" or ext == ".JPG" or ext == ".JPEG" or ext == ".png" or ext == ".PNG" or ext == ".gif" or ext == ".GIF":
			print "Image: " + image
			im = Image.open(location + "/" + image, 'r')
		
			w , h = im.size
			nim = im.resize((200, (200*h)/w))
		
			nim.convert('RGB').save(location + "/output-epub/" + newname + ".jpg", 'JPEG', dpi=(72,72), quality = opts["quality"])

if __name__ == "__main__": 
	main()
