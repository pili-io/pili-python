# -*- coding: utf-8 -*-

from pili import Mac, Hub

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "..."

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "..."

hub_name = '...'

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

resp = hub.wm_crete(name="test1", comment="for_test1", left='50%',
                    top='50%', width='10%', imageURL="http://xxx.xxx.com/abc.png")

print(resp.status_code)
print(resp.headers)
print(resp.text)
