#!/usr/bin/env python
"""Usage: ./test.py YOUR_SEZNAM_LOGIN YOUR_PASSWORD"""

import sys
from sklik import Client

url = 'https://api.sklik.cz/sandbox/bajaja/RPC2'
login = '%s@seznam.cz' % sys.argv[1]
password = sys.argv[2]

with Client(url, login, password, loglevel=2) as c:
    c.api.version()
    c.client.getAttributes()
    c.listReports()
