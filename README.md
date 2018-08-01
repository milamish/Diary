[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/c26c9b378e37231fc690)
[![Build Status](https://travis-ci.org/milamish/Diary.svg?branch=challenge3)](https://travis-ci.org/milamish/Diary)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Maintainability](https://api.codeclimate.com/v1/badges/9be8a79596c8225ef1b1/maintainability)](https://codeclimate.com/github/milamish/Diary/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/milamish/Diary/badge.svg?branch=challenge3)](https://coveralls.io/github/milamish/Diary?branch=challenge3)
# Diary
my diary app

set up a database environment
```
install postgress database
```
```
name the database diary and use milamish8 as password
```
install virtual environment
```
py -3 -m venv venv (for windows)
```
activate virtual environment
```
venv\Scripts\activate
```
install flask
```
pip install flask
```
enable database connection
```
pip install psycopg2
```
install requirements.txt
```
pip install -r requirements.txt
```
run the code from the run.py file

open postman to test on the functionality of the endpoints
```
home '/api/v2/'
registration '/api/v2/auth/signup'
login '/api/v2/auth/login'
post entry '/api/v2/entries'
fetch all entries '/api/v2/entries'
update entry '/api/v2/entries/<int:entry_id>'
delete entry '/api/v2/entries/<int:entry_id>'
view a single entry '/entry/<int:entry_id'
logout '/api/v2/logout'
```

copy the url then post it on postman

check on endpoint functionality by typing the required routes on postman and the methods as well