from flask import *
import unittest
import json

import os,sys
sys.path.insert(0, os.path.abspath(".."))

from __init__ import *

class Test_Diary(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	def test_Home(self):
		self.assertEqual(app.test_client().get('/api/v2/',).status_code,200)

	def test_login(self):
		m=app.test_client()
		response=(m.get('/api/v2/auth/login',).status_code, 500)

	def test_register(self):
		response=(app.test_client().get('/api/v2/auth/signUp,').status_code,500)
		respone2=(app.test_client().get('/api/v2/auth/signUp,').status_code,409)



if __name__ =='__main__':
    unittest.main()
