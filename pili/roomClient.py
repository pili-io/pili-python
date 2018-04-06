import hmac
import hashlib
import json
import time

import pili.api as api
from .utils import urlsafe_base64_encode, b
from .conf import RTC_API_HOST, RTC_API_VERSION


class RoomClient(object):
    """docstring for RoomClient"""
    def __init__(self, credentials):
        self.__credentials__ = credentials
        self.__auth__ = credentials.__auth__

    def create_room(self, ownerId, roomName=None, version=RTC_API_VERSION):
        params = {'owner_id': ownerId}
        url = "http://%s/%s/rooms" % (RTC_API_HOST, version)
        if bool(roomName):
            params['room_name'] = roomName
        encoded = json.dumps(params)
        return api._post(url=url, auth=self.__auth__, data=encoded)

    def getRoom(self, roomName, version=RTC_API_VERSION):
        url = "http://%s/%s/rooms/%s" % (RTC_API_HOST, version, roomName)
        return api._get(url=url, auth=self.__auth__)

    def deleteRoom(self, roomName, version=RTC_API_VERSION):
        url = "http://%s/%s/rooms/%s" % (RTC_API_HOST, version, roomName)
        return api._delete(url=url, auth=self.__auth__)

    def getUser(self, roomName, version=RTC_API_VERSION):
        url = "http://%s/%s/rooms/%s/users" % (RTC_API_HOST, version, roomName)
        return api._get(url=url, auth=self.__auth__)

    def kickUser(self, roomName, userId, version=RTC_API_VERSION):
        url = "http://%s/%s/rooms/%s/users/%s" % (RTC_API_HOST, version, roomName, userId)
        return api._delete(url=url, auth=self.__auth__)

    def roomToken(self, roomName, userId, perm, expireAt, version=RTC_API_VERSION):
        if version == RTC_API_VERSION:
            params = {"version": "2.0", "room_name": roomName,
                      "user_id": userId, "perm": perm,
                      "expire_at": int(time.time()) + expireAt}
        else:
            params = {"room_name": roomName,
                      "user_id": userId, "perm": perm,
                      "expire_at": int(time.time()) + expireAt}

        room_access_string = json.dumps(params, separators=(',', ':'))
        encoded_room_access = urlsafe_base64_encode(room_access_string)
        hashed = hmac.new(self.__auth__.secret_key, b(encoded_room_access), hashlib.sha1)
        encoded_sign = urlsafe_base64_encode(hashed.digest())
        return self.__auth__.access_key+":"+encoded_sign+":"+encoded_room_access
