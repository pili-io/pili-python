# -*- coding: utf-8 -*-

"""
https://developer.qiniu.com/pili/api/2777/save-the-live-playback
录制直播回放
"""


from pili import Mac, Hub

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "..."

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "..."

hub_name = "..."

stream_name = "123"

fname = 'example_fname.m3u8'

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

stream = hub.get(stream_name)

resp = stream.saveas(start=0, end=0, format='m3u8', fname=fname)

print(resp.status_code)
print(resp.headers)
print(resp.text)
