from flask import *
import diary
from diary import *
import unittest
import json

class Test_Diary(unittest.TestCase):

    def test_Home(self):
        self.assertEqual(app.test_client().get('/api/v1/home',).status_code,200)

    def test_entries(self):
        m=app.test_client()
        response=m.get('/api/v1/entry',)
        self.assertEqual(response.status_code,500)

    def test_fetchEntries(self):
        with app.test_client() as m:
            self.assertEqual(m.get('/api/v1/fetch_entries',).status_code,200)

    def test_updateEntry(self):
        m=app.test_client()
        self.assertEqual(m.get('/api/v1/update_entry',).status_code,404)

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

