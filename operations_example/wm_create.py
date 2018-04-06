# -*- coding: utf-8 -*-

"""
name:       模版名称, ^[A-Za-z0-9-_]{4,64}$
comment:    模版描述
left:       水印图片左上角距离视频图像左上角的水平位置占视频宽度的百分比，[0%, 100%)
top:        水印图片左上角距离视频图像左上角的垂直位置占视频 度的百分比，[0%, 100%)
width:      水印图片的宽度占视频宽度的百分比，高度会等比缩放。[0%, 100%), 与left之和不能超过100
imageURL:   水印图片地址，仅支持PNG格式
imageData:  base64编码的图片原始数据，与imageURL二选一!
"""

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
