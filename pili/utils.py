"""
Utils
"""

import contextlib
import json
import hmac
import hashlib
from base64 import urlsafe_b64encode, urlsafe_b64decode
from copy import deepcopy

from .compat import urlopen, HTTPError, b, s
from .errors import APIError


def send_and_decode(req):
    """
    Send the request and return the decoded json of response.

    Args:
        req: urllib2.Request

    Returns:
        A dict of decoded response
    """
    try:
        with contextlib.closing(urlopen(req)) as res:
            if res.getcode() == 204:
                return None
            raw = res.read()
            return json.loads(raw)
    except HTTPError as res:
        raw = res.read()
        try:
            data = json.loads(raw)
        except ValueError:
            raise APIError(res.reason)
        else:
            raise APIError(data["error"])


def __hmac_sha1__(data, key):
    """
    hmac-sha1
    """
    data = b(data)
    hashed = hmac.new(key, data, hashlib.sha1)
    return urlsafe_base64_encode(hashed.digest())


def urlsafe_base64_encode(data):
    ret = urlsafe_b64encode(b(data))
    return s(ret)


def urlsafe_base64_decode(data):
    ret = urlsafe_b64decode(s(data))
    return ret

def normalize_path(args, keyword, url):
    if set(args) - set(keyword):
        raise ValueError('invalid key')
    path = ''
    for k, v in args.items():
        if v:
            path += "&%s=%s" % (k, v)
    if path:
        url = url + '?' + path[1:]
    return url


def normalize_data(args, keyword):
    if set(args) - set(keyword):
        raise ValueError('invalid key')
    copy_args = deepcopy(args)
    for k, v in args.items():
        if not v:
            del copy_args[k]
    return json.dumps(copy_args)
