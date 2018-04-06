# -*- coding: utf-8 -*-

import json


import pili.api as api
from .utils import urlsafe_base64_encode
from .conf import API_HOST, API_VERSION
from .utils import normalize_path, normalize_data


class Stream(object):
    """
    Stream属性
        hub: 字符串类型，hub名字
        key: 字符串类型，流名
        disabledTill: 整型，Unix时间戳，在这之前流均不可用，-1表示永久不可用
        converts: 字符串数组，流的转码规格
    """
    def __init__(self, auth, hub, key):
        self.__auth__ = auth
        if not (hub and key):
            raise ValueError('invalid key')
        self.key = key
        self.hub = hub
        self.__data__ = None

    def __getattr__(self, attr):
        if not self.__data__:
            self.refresh()
        try:
            return self.__data__ if attr == "data" else self.__data__[attr]
        except KeyError as e:
            return e

    def __repr__(self):
        return self.to_json()

    # refresh 主动更新流信息，会产生一次rpc调用
    def refresh(self):
        key = urlsafe_base64_encode(self.key)
        url = "http://%s/%s/hubs/%s/streams/%s" % (API_HOST, API_VERSION, self.hub, key)
        data = api._get(url=url, auth=self.__auth__)
        self.__data__ = {}
        for p in ["disabledTill", "converts", "createdAt", "updatedAt", "expireAt", "watermark", "converts"]:
            self.__data__[p] = json.loads(data.text).get(p) if p in data.text else None
        self.__data__["key"] = self.key
        self.__data__["hub"] = self.hub
        return self.__data__

    # disable 禁用流，till Unix时间戳，在这之前流均不可用
    def disable(self, till=None):
        key = urlsafe_base64_encode(self.key)
        url = "http://%s/%s/hubs/%s/streams/%s/disabled" % (API_HOST, API_VERSION, self.hub, key)
        encoded = json.dumps({"disabledTill": till})
        return api._post(url=url, data=encoded, auth=self.__auth__)

    """
    status 查询直播信息
    返回值:
        startAt: 直播开始的Unix时间戳
        clientIP: 推流的客户端IP
        bps: 正整数 码率
        fps:
            audio: 正整数，音频帧率
            video: 正整数，视频帧率
            data: 正整数，数据帧率
    """
    def status(self):
        key = urlsafe_base64_encode(self.key)
        url = "http://%s/%s/hubs/%s/streams/%s/live" % (API_HOST, API_VERSION, self.hub, key)
        return api._get(url=url, auth=self.__auth__)

    """
    history 查询直播历史
    输入参数:
        start: Unix时间戳，起始时间，可选，默认不限制起始时间
        end: Unix时间戳，结束时间，可选，默认为当前时间
    返回值: 如下结构的数组
        start: Unix时间戳，直播开始时间
        end: Unix时间戳，直播结束时间
    """
    def history(self, **kwargs):
        key = urlsafe_base64_encode(self.key)
        keyword = ['start', 'end']
        url = "http://{0}/{1}/hubs/{2}/streams/{3}/historyactivity?".format(API_HOST, API_VERSION, self.hub, key)
        url = normalize_path(kwargs, keyword, url)
        return api._get(url=url, auth=self.__auth__)

    # save_as等同于saveas接口，出于兼容考虑，暂时保留
    def save_as(self, **kwargs):
        return self.saveas(**kwargs)

    """
    saveas 保存直播回放到存储空间
    输入参数:
        start: Unix时间戳，起始时间，可选，默认不限制起始时间
        end: Unix时间戳，结束时间，可选，默认为当前时间
        fname: 保存的文件名，可选，不指定会随机生产
        format: 保存的文件格式，可选，默认为m3u8，如果指定其他格式则保存动作为异步模式
        pipeline: dora的私有队列，可选，不指定则使用默认队列
        notify: 保存成功后的回调通知地址
        expireDays:  对应ts文件的过期时间
                    -1 表示不修改ts文件的expire属性
                    0  表示修改ts文件生命周期为永久保存
                    >0 表示修改ts文件的的生命周期为expireDay
    返回值:
        fname: 保存到存储空间的文件名
        persistentID: 异步模式时，持久化异步处理任务ID，通常用不到该字段
    """
    def saveas(self, **kwargs):
        key = urlsafe_base64_encode(self.key)
        url = "http://%s/%s/hubs/%s/streams/%s/saveas" % (API_HOST, API_VERSION, self.hub, key)
        keyword = ['start', 'end', 'fname', 'format', 'pipeline', 'notify', 'expireDays']
        encoded_data = normalize_data(kwargs, keyword)
        return api._post(url=url, auth=self.__auth__, data=encoded_data)

    """
    snapshot 保存直播截图到存储空间
    输入参数:
        time: Unix时间戳，要保存的时间点，默认为当前时间
        fname: 保存的文件名，可选，不指定会随机生产
        format: 保存的文件格式，可选，默认为jpg
    返回值:
        fname: 保存到存储空间的文件名
    """
    def snapshot(self, **kwargs):
        keyword = ['time', 'fname', 'format']
        encoded_data = normalize_data(kwargs, keyword)
        key = urlsafe_base64_encode(self.key)
        url = "http://%s/%s/hubs/%s/streams/%s/snapshot" % (API_HOST, API_VERSION, self.hub, key)
        return api._post(url=url, auth=self.__auth__, data=encoded_data)

    """
    update_converts 更改流的转码规格
    输入参数:
        profiles: 字符串数组，实时转码规格
    返回值: 无
    """
    def update_converts(self, profiles=[]):
        key = urlsafe_base64_encode(self.key)
        url = "http://%s/%s/hubs/%s/streams/%s/converts" % (API_HOST, API_VERSION, self.hub, key)
        encoded_data = json.dumps({"converts": profiles})
        return api._post(url=url, auth=self.__auth__, data=encoded_data)

    def to_json(self):
        return json.dumps(self.data)
