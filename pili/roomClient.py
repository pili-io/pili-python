import hmac
import hashlib
import json
import time
import pili.api as api
from utils import urlsafe_base64_encode

from conf import RTC_API_HOST


class RoomClient(object):
    """docstring for RoomClient"""
    def __init__(self, credentials):
        self.__credentials__ = credentials
        self.__auth__ = credentials.__auth__

    def create_room(self, ownerId, roomName=None, version='v2'):
        params = {'owner_id': ownerId}
        url = "http://%s/%s/rooms" % (RTC_API_HOST, version)
        if bool(roomName):
            params['room_name'] = roomName
        encoded = json.dumps(params)
        return api._post(url=url, auth=self.__auth__, data=encoded)

    def getRoom(self, roomName, version='v2'):
        url = "http://%s/%s/rooms/%s" % (RTC_API_HOST, version, roomName)
        return api._get(url=url, auth=self.__auth__)

    def deleteRoom(self, roomName, version='v2'):
        url = "http://%s/%s/rooms/%s" % (RTC_API_HOST, version, roomName)
        return api._delete(url=url, auth=self.__auth__)

    def getUser(self, roomName, version='v2'):
        url = "http://%s/%s/rooms/%s/users" % (RTC_API_HOST, version, roomName)
        return api._get(url=url, auth=self.__auth__)

    def kickUser(self, roomName, userId, version='v2'):
        url = "http://%s/%s/rooms/%s/users/%s" % (RTC_API_HOST, version, roomName, userId)
        return api._delete(url=url, auth=self.__auth__)

    def roomToken(self, roomName, userId, perm, expireAt, version='v2'):
        if version == 'v2':
            params = {"version": "2.0", "room_name": roomName,
                      "user_id": userId, "perm": perm,
                      "expire_at": int(time.time()) + expireAt}
        else:
            params = {"room_name": roomName,
                      "user_id": userId, "perm": perm,
                      "expire_at": int(time.time()) + expireAt}

        roomAccessString = json.dumps(params, separators=(',', ':'))
        encodedRoomAccess = urlsafe_base64_encode(roomAccessString)
        hashed = hmac.new(self.__auth__.secret_key, encodedRoomAccess, hashlib.sha1)
        encodedSign = urlsafe_base64_encode(hashed.digest())
        return self.__auth__.access_key+":"+encodedSign+":"+encodedRoomAccess
