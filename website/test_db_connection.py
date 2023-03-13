
import os
from pathlib import Path

from django.db import connections
from django.db.utils import OperationalError

BASE_DIR = Path(__file__).resolve().parent.parent


db_conn = connections['default']
try:
    c = db_conn.cursor()
except OperationalError:
    isConnected = False
else:
    isConnected = True



#if isConnected == False:
 #   if os.path.isfile(BASE_DIR + "/db.sqlite3"):
  #      isConnected = True



if(isConnected):
    print("connected")
else:
    print("not connect")
