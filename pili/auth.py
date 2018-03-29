"""
Auth provide class Auth for authentication account. You can use decorator
auth_interface to create a function with auto generated authentication.
"""

from .utils import __hmac_sha1__
from .compat import urlparse
import pili.conf as conf


class Mac(object):
    def __init__(self, access_key, secret_key):
        if not (access_key and secret_key):
            raise ValueError('invalid key')
        self.__auth__ = Auth(access_key, secret_key)


class Auth(object):
    """
    class Auth store the access_key and secret_key for authentication.
    """
    def __init__(self, access_key, secret_key):
        if not (access_key and secret_key):
            raise ValueError('invalid key')
        self.access_key, self.secret_key = access_key, secret_key

    def auth_interface_str(self, raw_str):
        """
        generate sign str.
        """
        encoded = __hmac_sha1__(raw_str, self.secret_key)
        return 'Qiniu {0}:{1}'.format(self.access_key, encoded)

    def authed(self, method, url, body=None):
        headers = {}

        parsed = urlparse(url)
        raw_str = '%s %s' % (method, parsed.path)
        if parsed.query:
            raw_str += '?%s' % parsed.query
        raw_str += '\nHost: %s' % parsed.netloc
        if body:
            raw_str += '\nContent-Type: application/json'
            raw_str += "\n\n"
            raw_str += body
            headers.update({'Content-Type': 'application/json'})
        else:
            raw_str += "\n\n"
        headers.update({'Authorization': self.auth_interface_str(raw_str)})
        headers.update({'User-Agent': conf.API_USERAGENT})
        return headers

