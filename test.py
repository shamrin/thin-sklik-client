#!/usr/bin/env python

import sys
from sklik import Client

url = 'https://api.sklik.cz/bajaja/RPC2'
login = '%s@seznam.cz' % sys.argv[1]
password = sys.argv[2]

with Client(url, login, password, debug=True) as client:
    client.listReports()
