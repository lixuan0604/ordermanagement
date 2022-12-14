from django.test import TestCase

# Create your tests here.


import datetime,time

timee = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timee)


# strr = ''
#
# spli = strr.split(',')
# for i in spli:
#


import time
from datetime import datetime

def get_india_timestamp():
    local_offset = time.localtime().tm_gmtoff   # 当前机器utc时间偏移量
    print('local_offset',local_offset)
    india_offset = int(5.5 * 60*60)
    offset = local_offset - india_offset
    timestamp = int(datetime.now().timestamp())
    india_timestamp = timestamp - offset

    return india_timestamp

india_timestamp = get_india_timestamp()
print(datetime.fromtimestamp(india_timestamp))