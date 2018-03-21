# -*- coding: utf-8 -*-

from pili import Mac, Hub

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "Y93_QIW2j-Bw84R7M07Mnno0re7TcEFq1InWpc9J"

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "BVclqX13x3uhr099JXcrfZS__wyF2fUnBFW4Kj5G"

hub_name = 'berniezhibo'

stream_name = '123'

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

stream = hub.get(stream_name)

resp = stream.history(start_second=3123123, end_second=3123123123)

print(resp.status_code)
print(resp.headers)
print(resp.text)
