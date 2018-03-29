# -*- coding: utf-8 -*-
import time
from pili import Mac, Hub

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "..."

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "..."

hub_name = '...'

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

resp = hub.bandwidth_count_history(start=int(time.time())-100,
                                   end=int(time.time()), limit=100, marker=None)

print(resp.status_code)
print(resp.headers)
print(resp.text)
