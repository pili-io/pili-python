# -*- coding: utf-8 -*-

from pili import Mac, Hub, rtmp_play_url, rtmp_publish_url, hdl_play_url, hls_play_url, snapshot_play_url

# 替换成自己 Qiniu 账号的 AccessKey
access_key = "..."

# 替换成自己 Qiniu 账号的 SecretKey
secret_key = "..."

domain = '...'

hub_name = '...'

stream_name = '...'

expire = 3600

mac = Mac(access_key, secret_key)

hub = Hub(mac, hub_name)

stream = hub.get(stream_name)


print rtmp_publish_url(domain, hub_name, stream_name, mac, expire)

print rtmp_play_url(domain, hub_name, stream_name)

print hls_play_url(domain, hub_name, stream_name)

print hdl_play_url(domain, hub_name, stream_name)

print snapshot_play_url(domain, hub_name, stream_name)
