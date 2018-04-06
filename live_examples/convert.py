# -*- coding: utf-8 -*-

"""
https://developer.qiniu.com/pili/api/2521/modify-the-flow-configuration
修改转码流配置
"""


from pili import Mac, Hub

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "..."

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "..."

hub_name = "..."

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

stream = hub.get("123")

resp = stream.update_converts(["480p", "720p"])

# 建议打印headers，方便向官方反馈问题，该接口调用成功会返回json为空{}
print(resp.status_code)
print(resp.headers)
print(resp.text)
