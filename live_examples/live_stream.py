# -*- coding: utf-8 -*-

"""
https://developer.qiniu.com/pili/api/2776/live-broadcast-of-real-time-information
单条流实时状态查询
"""


from pili import Mac, Hub

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "..."

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "..."

hub_name = "..."

stream_name = "123"

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

stream = hub.get(stream_name)

resp = stream.status()

print(resp.status_code)
print(resp.headers)
print(resp.text)
