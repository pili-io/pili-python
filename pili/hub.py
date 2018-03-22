# -*- coding: utf-8 -*-

import pili.api as api
from .stream import Stream
from conf import API_HOST, API_VERSION
from utils import normalize_path, normalize_data
import json

class Hub(object):
    def __init__(self, mac, hub):
        self.__auth__ = mac.__auth__
        self.__hub__ = hub

    # create 创建一路流
    def create(self, **kwargs):
        keyword = ['key']
        url = "http://%s/%s/hubs/%s/streams" % (API_HOST, API_VERSION, self.__hub__)
        encoded = normalize_data(kwargs, keyword)
        return api._post(url=url, auth=self.__auth__, data=encoded)


    # 获取一路流
    def get(self, key):
        return Stream(self.__auth__, hub=self.__hub__, key=key)

    """
    list 遍历hub的流列表
    输入参数:
        prefix: 字符串，匹配的流名前缀
        liveonly: 布尔值，可选，如果为True则只列出正在直播的流
        limit: 正整数，限定了一次最多可以返回的流个数，实际返回的流个数可能会小于这个值
        marker: 字符串，上一次遍历得到的游标
    返回值:
        items: 字符串数组，查询返回的流名
        marker: 这次遍历得到的游标，下次请求应该带上，如果为""，则表示已遍历完所有流
    """
    def list(self, **kwargs):
        url = "http://%s/%s/hubs/%s/streams?" % (API_HOST, API_VERSION, self.__hub__)
        keyword = ['liveonly', 'prefix', 'limit', 'marker']
        url = normalize_path(kwargs, keyword, url)
        return api._get(url=url, auth=self.__auth__)


    """
    batch_live_status 批量查询流的直播信息
    输入参数:
        streams: 要查询的流名数组，长度不能超过100
    返回值: 如下结构体的数组
        key: 流名
        startAt: 直播开始的Unix时间戳
        clientIP: 推流的客户端IP
        bps: 正整数 码率
        fps:
            audio: 正整数，音频帧率
            video: 正整数，视频帧率
            data: 正整数，数据帧率
    """
    def batch_live_status(self, streams):
        encoded = json.dumps({"items": streams})
        url = "http://%s/%s/hubs/%s/livestreams?" % (API_HOST, API_VERSION, self.__hub__)
        return api._post(url=url, auth=self.__auth__, data=encoded)


    def bandwidth_count_now(self):
        url = "http://%s/%s/hubs/%s/stat/play" % (API_HOST, API_VERSION, self.__hub__)
        return api._get(url, self.__auth__)

    def bandwidth_count_history(self, **kwargs):
        url = "http://%s/%s/hubs/%s/stat/play/history?" % (API_HOST, API_VERSION, self.__hub__)
        keyword = ['start', 'end', 'limit', 'marker']
        url = normalize_path(kwargs, keyword, url)
        return api._get(url=url, auth=self.__auth__)

    def bandwidth_count_detail(self, time):
        url = "http://%s/%s/hubs/%s/stat/play/history/detail?time=%s" % (API_HOST, API_VERSION, self.__hub__, time)
        return api._get(url, self.__auth__)

