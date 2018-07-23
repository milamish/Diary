from flask import *
import diary3
from diary3 import *
import unittest
import json

class Test_Diary3(unittest.TestCase):

	def test_Home(self):
		self.assertEqual(app.test_client().get('/api/v2/home',).status_code,200)

	def test_login(self):
		m=app.test_client()
		response=(m.get('/api/v2/login',).status_code, 500)




if __name__ =='__main__':
    unittest.main()
