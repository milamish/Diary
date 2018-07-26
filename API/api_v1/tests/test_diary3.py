from flask import *
import unittest
import json

from __init__ import *

class Test_Diary3(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	def test_Home(self):
		self.assertEqual(app.test_client().get('/api/v2/home',).status_code,200)

	def test_login(self):
		m=app.test_client()
		response=(m.get('/api/v2/login',).status_code, 500)

	def test_register(self):
		m=app.test_client()
		response=(m.get('/api/v2/register,').status_code,500)

	def test_modify_an_entry(self):
		self.assertEqual(app.test_client().get('/api/v2/modify_an_entry,').status_code,404)

	def test_delete_entry(self):
		m= app.test_client()
		response=(m.get('/api/v2/delete_entry,').status_code,403)

	def test_view_entries(self):
		m=app.test_client()
		response=(m.get('/api/v2/view_all_entries,').status_code,403)
		response2=(m.get('/api/v2/view_all_entries,').status_code,200)



if __name__ =='__main__':
    unittest.main()
