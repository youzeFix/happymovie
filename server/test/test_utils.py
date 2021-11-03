import unittest
from server.utils import datetime_to_json
import json
import datetime

class TestUtilsMethods(unittest.TestCase):

    def test_datetime_to_json(self):
        obj = datetime.datetime.now()

        print(json.dumps({'aaa':obj}, default=datetime_to_json))