from django.db import connections
from django.db.utils import OperationalError

db_conn = connections['default']
try:
    c = db_conn.cursor()
except OperationalError:
    if OperationalError: 
        isConnected = False
    # else:
    #     if


else:
    isConnected = True


if(isConnected):
    print("connected")
else:
    print("not connect")
