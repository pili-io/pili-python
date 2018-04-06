# -*- coding: utf-8 -*-

"""
https://developer.qiniu.com/pili/api/2778/live-history
单个直播流历史查询
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

resp = stream.history(start=1513616430, end=1513616400)

print(resp.status_code)
print(resp.headers)
print(resp.text)
