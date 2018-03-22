# -*- coding: utf-8 -*-

"""
https://developer.qiniu.com/pili/api/2520/save-the-live-capture
"""

from pili import Mac, Hub

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "..."

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "..."

hub_name = '...'

stream_name = "..."

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

stream = hub.get(stream_name)

# 不填参数或till为0表示不禁播，-1表示永久禁播，其他数字表示禁播到某一时刻的时间戳
resp = stream.snapshot(time=1521710848, fname="123.jpg", format="jpg")

print(resp.status_code)
print(resp.headers)
print(resp.text)



