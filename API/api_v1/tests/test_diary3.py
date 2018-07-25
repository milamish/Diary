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

	def test_register(self):
		m=app.test_client()
		response=(m.get('/api/v2/register,').status_code,500)

	def test_modify_an_entry(self):
		self.assertEqual(app.test_client().get('/api/v2/modify_an_entry,').status_code,404)

	def test_register(self):
		m=app.test_client()
		json_response=m.post(('/api/v2/register'),data={
			'name':'mildred',
			'username':'milamish',
			'password':'mish',
			'repeat_password':'mish',
			'email_adress':'milamish@yahoo.com'
			})
		self.assertTrue(response.status_code==302)



if __name__ =='__main__':
    unittest.main()
