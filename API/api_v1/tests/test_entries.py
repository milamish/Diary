from flask import *
import unittest
import json

import os,sys
sys.path.insert(0, os.path.abspath(".."))

from __init__ import *

class Test_Diary3(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
	
	def test_modify_an_entry(self):
		self.assertEqual(app.test_client().get('/api/v2/entries,').status_code,404)

	def test_delete_entry(self):
		m= app.test_client()
		response=(m.get('/api/v2/entries,').status_code,403)

	def test_view_entries(self):
		m=app.test_client()
		response=(m.get('/api/v2/entries,').status_code,403)
		response2=(m.get('/api/v2/entries,').status_code,200)

	def test_single_entries(self):
		self.assertEqual(app.test_client().get('/api/v2/entry,').status_code,404)

	def test_add_entry(self):
		self.assertEqual(app.test_client().get('/api/v2/entries,').status_code,404)

if __name__ =='__main__':
    unittest.main()
