# -*- coding: utf-8 -*-

import os
import unittest
import time
import random
import json

from pili import Hub, Mac
from pili.conf import API_HOST


def env(key):
    if key in os.environ:
        return os.environ[key]
    else:
        return ""


class TestHubCases(unittest.TestCase):

    def setUp(self):
        hub_name = env("TEST_HUB")
        access_key = env("access_key")
        secret_key = env("secret_key")

        if access_key == "" or secret_key == "":
            raise unittest.SkipTest("need set access_key or secret_key")
        if env("PILI_API_HOST") != "":
            API_HOST = env("PILI_API_HOST")
        mac = Mac(access_key, secret_key)
        self.hub = Hub(mac, hub_name)

    # 这个测试case需要保持推流test1
    def test_batch_live_status(self):
        items = self.hub.batch_live_status(["test1", "test2"])
        self.assertEqual(items.status_code, 200)
        self.assertIn("test1", json.loads(items.text).get("items")[0].get("key"))

    def test_create_strean(self):
        items = self.hub.create(key="streamtest" + str(int(random.random()*1e10))+str(time.time())[:10])
        self.assertEqual(items.status_code, 200)
        self.assertEqual({}, json.loads(items.text))

