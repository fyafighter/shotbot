import os
import tempfile
import pytest
from flask import Flask, jsonify, request, json
from server import app
import unittest
from bot import Bot

class TestServer(unittest.TestCase):
    app = app.test_client()
    def test_is_online(self):
        response = self.app.get('/status')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_data['status'], "online")
    
    def test_targets(self):
        response = self.app.get('/target')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_data['target'], [2,2])
        response = self.app.put('/target', data=jsonify(target=[3,3]))
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_data['target'], [3,2])

