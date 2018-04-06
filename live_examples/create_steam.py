# -*- coding: utf-8 -*-

"""
https://developer.qiniu.com/pili/api/2515/create-a-flow
创建流
"""


from pili import Mac, Hub

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "..."

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "..."

hub_name = "..."

stream_name = "..."

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

resp = hub.create(key=stream_name)

print(resp.status_code)
print(resp.headers)
print(resp.text)

print(hub.get(stream_name))
