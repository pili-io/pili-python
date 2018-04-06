# -*- coding: utf-8 -*-

"""
https://developer.qiniu.com/pili/api/3764/batch-query-broadcast-real-time-information
批量获取实时流信息
"""

from pili import Mac, Hub

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "..."

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "..."

hub_name = "..."

stream_lists = ["123", "abc"]

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

resp = hub.batch_live_status(stream_lists)

print(resp.status_code)
print(resp.headers)
print(resp.text)
