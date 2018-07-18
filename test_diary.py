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

    def test_viewHobbies(self):
        with app.test_client() as m:
            response=m.get('/api/v1/view_hobbies',)
            self.assertEqual(response.status_code, 403)

    def test_viewAchievement(self):
        with app.test_client() as m:
            response=m.get('api/v1/view_achievement',)
            self.assertEqual(response.status_code, 403)

    def test_allUsers(self):
        with app.test_client() as m:
            response=m.get('api/v1/all_users',)
            self.assertEqual(response.status_code,403)



        

if __name__ =='__main__':
    unittest.main()

