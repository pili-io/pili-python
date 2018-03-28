from .auth import auth_interface
import pili.conf as conf
from requests import Request
import requests
import json
import base64
# from compat import urlparse
#
#
# def normalize(args, keyword):
#     if set(args) - set(keyword):
#         raise ValueError('invalid key')
#     for k, v in args.items():
#         if v is None:
#             del args[k]
#     return args
#
#
@auth_interface
def delete_room(version, roomName):
    url = "http://%s/%s/rooms/%s" % (conf.RTC_API_HOST, version, roomName)
    req = Request(url=url)
    req.get_method = lambda: 'DELETE'
    return req


@auth_interface
def get_room(version, roomName):
    url = "http://%s/%s/rooms/%s" % (conf.RTC_API_HOST, version, roomName)
    return Request(url=url)


@auth_interface
def get_user(version, roomName):
    url = "http://%s/%s/rooms/%s/users" % (conf.RTC_API_HOST, version, roomName)
    return Request(url=url)


@auth_interface
def kick_user(version, roomName, userId):
    url = "http://%s/%s/rooms/%s/users/%s" % (conf.RTC_API_HOST, version, roomName, userId)
    req = Request(url=url)
    req.get_method = lambda: 'DELETE'
    return req


@auth_interface
def create_room(ownerId, version, roomName=None):
    params = {'owner_id': ownerId}
    url = "http://%s/%s/rooms" % (conf.RTC_API_HOST, version)
    if bool(roomName):
        params['room_name'] = roomName
    encoded = json.dumps(params)
    req = Request(url=url, data=encoded)
    req.get_method = lambda: 'POST'
    return req


def _get(url, auth):
    print("get")
    hearders = auth.authed("GET", url)
    return requests.get(url=url, headers=hearders)


def _post(url, auth, data):
    print("post")
    hearders = auth.authed("POST", url, body=data)
    return requests.post(url=url, headers=hearders, data=data)

def _delete(url, auth):
    print("delete")
    hearders = auth.authed("DELETE", url)
    return requests.delete(url=url, headers=hearders)