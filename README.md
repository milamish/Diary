[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/c26c9b378e37231fc690)
[![Build Status](https://travis-ci.org/milamish/Diary.svg?branch=challenge2)](https://travis-ci.org/milamish/Diary)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Maintainability](https://api.codeclimate.com/v1/badges/9be8a79596c8225ef1b1/maintainability)](https://codeclimate.com/github/milamish/Diary/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/milamish/Diary/badge.svg?branch=master)](https://coveralls.io/github/milamish/Diary?branch=master)
# Diary
my diary app

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
intall requirements.txt
```
pip freeze > requirements.txt
```
run the code

open postman to test on the functionality of the endpoints
```
home '/api/v1/home'
registration '/api/v1/register'
login '/api/v1/login'
post entry '/api/v1/entry'
fetch one entry '/api/v1/individual_entry/<int:ID>'
fetch all entries '/api/v1/fetch_entries'
update entry '/api/v1/update_entry/<int:ID>''
delete entry '/api/v1/delete_entry/<int:ID>'
```

copy the url then post it on postman

check on endpoint functionality by typing the required routes on postman and the methods as well