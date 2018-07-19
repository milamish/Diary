from flask import *
import diary
from diary import *
import unittest
import json

class Test_Diary(unittest.TestCase):

    def test_Home(self):
        with app.test_client() as m:
            response=m.get('/api/v1/home',)
            self.assertEqual(response.status_code,200)

    def test_entries(self):
        with app.test_client() as m:
            response=m.get('/api/v1/entry',)
            self.assertEqual(response.status_code,500)

    def test_fetchEntries(self):
        with app.test_client() as m:
            response=m.get('/api/v1/fetch_entries',)
            self.assertEqual(response.status_code,200)

    def test_updateEntry(self):
        with app.test_client() as m:
            response=m.get('/api/v1/update_entry',)
            self.assertEqual(response.status_code,404)

    def test_deleteEntry(self):
        with app.test_client() as m:
            response= m.get('/api/v1/delete_entry',)
            self.assertEqual(response.status_code,404)

    def test_register(self):
        with app.test_client() as m:
            response = m.get('api/v1/register',)
            self.assertEqual(response.status_code,500)

    def test_login(self):
        with app.test_client() as m:
            response=m.get('api/v1/login')
            self.assertEqual(response.status_code,500)

if __name__ =='__main__':
    unittest.main()

