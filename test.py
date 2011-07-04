#!/usr/bin/env python

from sklik import SklikProxy

url = 'https://api.sklik.cz/sandbox/bajaja/RPC2'
login = 'YOUR_LOGIN_HERE@seznam.cz'
password = 'YOUR_PASSWORD_HERE'

sklik = SklikProxy(url, debug=True)

sklik.client.login(login, password)
try:
    sklik.listReports()
finally:
    sklik.client.logout()
