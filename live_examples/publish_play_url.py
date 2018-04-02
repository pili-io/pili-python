# -*- coding: utf-8 -*-

"""
https://developer.qiniu.com/pili/api/2767/the-rtmp-push-flow-address
生成推流拉流及封面地址

该生成推流地址方法只适用于v2版本的限时鉴权，v2的无鉴权只需拼接域名，直播空间名和流名，v1版本的鉴权算法见下
https://developer.qiniu.com/pili/kb/1332/broadcast-authentication-mode
https://developer.qiniu.com/pili/kb/2635/seven-cows-live-push-flow-authentication-md
"""


from pili import Mac, Hub, rtmp_play_url, rtmp_publish_url, hdl_play_url, hls_play_url, snapshot_play_url

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "..."

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "..."

hub_name = "..."

domain = "..."

stream_name = '123'

expire = 3600

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

stream = hub.get(stream_name)

print(rtmp_publish_url(domain, hub_name, stream_name, mac, expire))

# print(rtmp_play_url(domain, hub_name, stream_name))
#
# print(hls_play_url(domain, hub_name, stream_name))
#
# print(hdl_play_url(domain, hub_name, stream_name))
#
# print(snapshot_play_url(domain, hub_name, stream_name))
