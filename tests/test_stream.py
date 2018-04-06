# -*- coding: utf-8 -*-

import os
import random
import time
from unittest import TestCase, SkipTest
from json import loads

from pili import Mac, Hub


def env(key):
    if key in os.environ:
        return os.environ[key]
    else:
        return ""


class TestStreamCases(TestCase):

    def setUp(self):
        hub_name = env("TEST_HUB")
        access_key = env("access_key")
        secret_key = env("secret_key")

        if access_key == "" or secret_key == "":
            raise SkipTest("need set access_key or secret_key")
        mac = Mac(access_key, secret_key)
        self.hub = Hub(mac, hub_name)
        self.stream_title = "streamTest" + str(int(random.random()*1e10))

    def test_stream_create(self):
        items = self.hub.create(key=self.stream_title)
        self.assertEqual(items.status_code, 200)
        self.assertEqual(loads(items.text), {})

    def test_stream_disable(self):
        self.hub.create(key=self.stream_title)
        stream = self.hub.get(key=self.stream_title)
        self.assertEqual({}, loads(stream.disable(-1).text))
        self.assertEqual(-1, stream.refresh().get("disabledTill"))
        stream.disable(0)
        self.assertEqual(0, stream.refresh().get("disabledTill"))

    def test_stream_converts(self):
        stream = self.hub.get(key="test1")
        stream.update_converts(["480p", "720p"])
        self.assertEqual(stream.converts, ["480p", "720p"])

    # 这个测试需要维持推流test1
    def test_stream_saveas(self):
        stream = self.hub.get("test1")
        ret = stream.save_as()
        self.assertEqual(200, ret.status_code)
        now = int(time.time())
        ret = stream.saveas(start=now - 3600)
        self.assertIn(ret.status_code, (200, 619))
        ret = stream.save_as(start=now - 3600, end=now)
        self.assertIn(ret.status_code, (200, 619))
        ret = stream.saveas(start=now - 3600, end=now, fname="test1.m3u8", format="m3u8")
        self.assertEqual(loads(ret.text).get("fname"), "test1.m3u8")
        ret = stream.save_as(start=now - 3600, end=now, fname="test1.mp4", format="mp4")
        self.assertEqual(loads(ret.text).get("fname"), "test1.mp4")
        self.assertTrue(loads(ret.text).get("persistentID"))

    # 这个测试需要维持推流test1
    def test_stream_snashot(self):
        stream = self.hub.get("test1")
        ret = stream.snapshot(fname="test1.jpg")
        self.assertEqual(loads(ret.text)["fname"], "test1.jpg")

    # 这个测试需要维持推流test1
    def test_stream_history(self):
        stream = self.hub.get("test1")
        self.assertEqual(200, stream.history().status_code)

