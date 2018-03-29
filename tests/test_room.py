# -*- coding: utf-8 -*-

import os
import unittest
import json

from pili import RoomClient, Mac


def env(key):
    if key in os.environ:
        return os.environ[key]
    else:
        return ""


class TestRoomCases(unittest.TestCase):

    def setUp(self):
        access_key = env("access_key")
        secret_key = env("secret_key")

        if access_key == "" or secret_key == "":
            raise unittest.SkipTest("need set access_key or secret_key")
        mac = Mac(access_key, secret_key)
        self.room = RoomClient(mac)

    def test_create_room(self):
        items = self.room.create_room('admin_user', 'roomname')
        self.assertEqual("roomname", json.loads(items.text).get("room_name"))

    def test_create_token(self):
        test_token = self.room.roomToken('roomname', 'admin_user', 'admin', 3600)
        import base64
        decode_token = json.loads(base64.decodestring(test_token.split(":")[2]))
        self.assertIn("admin_user", decode_token.get("user_id"))
        self.assertIn("2.0", decode_token.get("version"))
        self.assertIn("roomname", decode_token.get("room_name"))

    def test_delete_room(self):
        resp = self.room.deleteRoom("roomname")
        self.assertEqual({}, json.loads(resp.text))

    def test_query_room(self):
        resp = self.room.getRoom("roomname")
        decode_data = json.loads(resp.text)
        self.assertEqual("roomname", decode_data.get("room_name"))

    def test_query_user(self):
        resp = self.room.getUser(roomName="roomname")
        decode_data = json.loads(resp.text)
        self.assertIn("active_users", decode_data)


