import os
import time

minute = 60000
hour = minute * 60

while True:
    os.system('python3 scraper.py')
    time.sleep(hour)
    