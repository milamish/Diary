from flask import *
import unittest
import json

import os,sys
sys.path.insert(0, os.path.abspath(".."))

from __init__ import *

class Test_Diary3(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	def test_signed_in(self):
		sign_data=json.dumps({"username":"mish", "password":"Milamish"})
		header={"content-type":"application/json"}
		signedin=app.test_client().post('/api/v2/auth/login',data=sign_data, headers=header)
		response=signedin

	def test_view_access(self):
		token= self.test_signed_in()
		header={ "x-access-token":token}
		response=app.test_client().get('/api/v2/entries', headers=header)
		self.assertEqual(response.status_code, 200)
	
	def test_modify_an_entry(self):
		self.assertEqual(app.test_client().get('/api/v2/entries',).status_code,200)

	def test_delete_entry(self):
		m= app.test_client()
		response=(m.delete('/api/v2/entries',).status_code,403)

	def test_view_entries(self):
		m=app.test_client()
		response=(m.get('/api/v2/entries',).status_code,403)

	def test_single_entries(self):
		self.assertEqual(app.test_client().get('/api/v2/entries',).status_code,200)

	def test_add_entry(self):
		self.assertEqual(app.test_client().get('/api/v2/entries',).status_code,200)

if __name__ =='__main__':
    unittest.main()
