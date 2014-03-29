
# coding=UTF-8

from libre import * 
import unittest 



class TestLibreText(unittest.TestCase): 
	
	def setUp(self): 
		mytext = "ORIGINAL\n======test======\nAutor: test\n\n "
		self.libre = LibreText(mytext)

	def testGetters(self): 
		
		self.assertEqual(self.libre.getTitle(), "test") 
		self.assertEqual(self.libre.getAuthor(), "test")
		self.assertEqual(self.libre.getStatusString(), "ORIGINAL")

	def testSpecificCir(self): 
		mytext = "PROVEREN\n======PC = Windows?======\n\nАутор: Дејан Маглов\n"
		my = LibreText(mytext) 
		self.assertEqual(my.getTitle(), "PC = Windows?") 
		self.assertEqual(my.getAuthor(), "Дејан Маглов")
		self.assertEqual(my.getStatusString(), "PROVEREN")
unittest.main()
