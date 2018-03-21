# -*- coding: utf-8 -*-

from pili import Mac, Hub

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "..."

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "..."

hub_name = '...'

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

stream = hub.get("123")

resp = stream.update_converts(["480p", "720p"])

# 建议打印headers方便向官方反馈问题，该接口调用成功是放回json为空{}
print(resp.status_code)
print(resp.headers)
print(resp.text)


