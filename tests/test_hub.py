# -*- coding: utf-8 -*-

import os
import time
import random
from json import loads
from unittest import TestCase, SkipTest

from pili import Hub, Mac


def env(key):
    if key in os.environ:
        return os.environ[key]
    else:
        return ""


class TestHubCases(TestCase):

    def setUp(self):
        hub_name = env("TEST_HUB")
        access_key = env("access_key")
        secret_key = env("secret_key")

        if access_key == "" or secret_key == "":
            raise SkipTest("need set access_key or secret_key")
        mac = Mac(access_key, secret_key)
        self.hub = Hub(mac, hub_name)

    # 这个测试case需要保持推流test1
    def test_batch_live_status(self):
        items = self.hub.batch_live_status(["test1", "test2"])
        self.assertEqual(items.status_code, 200)
        self.assertIn("test1", loads(items.text).get("items")[0].get("key"))

    def test_create_stream(self):
        self.stream_key = "streamtest" + str(int(random.random()*1e10))+str(time.time())[:10]
        items = self.hub.create(key=self.stream_key)
        self.assertEqual(items.status_code, 200)
        self.assertEqual({}, loads(items.text))

    def test_query_streams(self):
        items = self.hub.get("test1")
        self.assertNotEqual(None, items)

    def test_wm_create(self):
        test_name = "test" + str(int(time.time()))
        items = self.hub.wm_crete(name=test_name, comment="for_test1", left='50%',
                    top='50%', width='10%', imageURL="http://omhrg3tgg.bkt.clouddn.com/413.png")
        self.assertEqual(items.status_code, 200)
        self.assertEqual(test_name, loads(items.text).get("name"))
        items1 = self.hub.wm_crete(name="test1", comment="for_test1", left='50%',
                    top='50%', width='10%', imageURL="http://omhrg3tgg.bkt.clouddn.com/413.png")
        self.assertEqual(items1.status_code, 614)

    def test_wm_download(self):
        item = self.hub.wm_download(name="test1522373806")
        self.assertEqual(item.status_code, 200)

    def test_wm_list(self):
        items = self.hub.wm_list(limit=100)
        self.assertIn("items", loads(items.text))

    def test_wm_query(self):
        items = self.hub.wm_query("test1")
        self.assertEqual("test1", loads(items.text).get("name"))

    def test_bandwidth_detail(self):
        items = self.hub.bandwidth_count_detail(str(int(time.time())))
        self.assertIn("items", loads(items.text))

    def test_bandwidth_history(self):
        items = self.hub.bandwidth_count_history(start=int(time.time()) - 100,
                                                 end=int(time.time()), limit=100, marker=None)
        self.assertIn("items", loads(items.text))

    def test_bandwidth_now(self):
        items = self.hub.bandwidth_count_now()
        self.assertIn("total", loads(items.text))
