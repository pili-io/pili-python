# -*- coding: utf-8 -*-

"""
https://developer.qiniu.com/pili/api/2773/query-stream
查询流详情
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

stream = hub.get(stream_name)

print(stream)


