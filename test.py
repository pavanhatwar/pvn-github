import time
import datetime


while True:
    ts = time.time()
    a = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print a
    time.sleep(1)
