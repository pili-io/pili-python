# -*- coding: utf-8 -*-

import os
import random
import time
import unittest
import json

from pili import Mac, Hub


def env(key):
    if key in os.environ:
        return os.environ[key]
    else:
        return ""


class TestStreamCases(unittest.TestCase):

    def setUp(self):
        hub_name = env("TEST_HUB")
        access_key = env("access_key")
        secret_key = env("secret_key")
        if access_key == "" or secret_key == "":
            raise unittest.SkipTest("need set access_key or secret_key")
        mac = Mac(access_key, secret_key)
        self.hub = Hub(mac, hub_name)
        self.stream_title = "streamTest" + str(int(random.random()*1e10))

    def test_stream_create(self):
        stream = self.hub.create(key=self.stream_title)
        self.assertEqual(stream.hub, "PiliSDKTest")
        self.assertEqual(stream.key, self.stream_title)

    def test_stream_disable(self):
        stream = self.hub.create(key=self.stream_title)
        self.assertEqual({}, json.loads(stream.disable(-1).text))
        self.assertEqual(-1, stream.refresh().get("disabledTill"))
        stream.disable(0)
        self.assertEqual(0, stream.refresh().get("disabledTill"))

    def test_stream_converts(self):
        stream = self.hub.create(key=self.stream_title)
        self.assertEqual(len(stream.converts), 0)
        stream.update_converts(["480p", "720p"])
        stream = stream.refresh()
        self.assertEqual(stream.converts, ["480p", "720p"])
        stream.update_converts()
        stream = stream.refresh()
        self.assertEqual(len(stream.converts), 0)

    # 这个测试需要维持推流test1
    def test_stream_saveas(self):
        stream = self.hub.get("test1")
        ret = stream.save_as()
        self.assertEqual(200, ret.status_code)
        now = int(time.time())
        ret = stream.saveas(start=now - 20)
        self.assertIn(ret.status_code, (200, 619))
        ret = stream.save_as(start=now - 20, end=now)
        self.assertIn(ret.status_code, (200, 619))
        ret = stream.saveas(start=now - 20, end=now, fname="test1.m3u8", format="m3u8")
        self.assertEqual("test1.m3u8", json.loads(ret.text).get("fname"))
        ret = stream.save_as(start=now - 20, end=now, fname="test1.mp4", format="mp4")
        self.assertEqual(ret["fname"], "test1.mp4")
        self.assertTrue(ret["persistentID"])

    # 这个测试需要维持推流test1
    def test_stream_snashot(self):
        stream = self.hub.get("test1")
        ret = stream.snapshot(fname="test1.jpg")
        self.assertEqual(json.loads(ret.text)["fname"], "test1.jpg")

    # 这个测试需要维持推流test1
    def test_stream_history(self):
        stream = self.hub.get("test1")
        self.assertEqual(200, stream.history().status_code)

