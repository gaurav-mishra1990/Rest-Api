import unittest
from apis.Log.routes import api as log_api
from flask import Flask
from flask_restplus import Api
import os
import json


def create_app():
    app = Flask(__name__)
    os.environ["FLASK_ENV"] = "testing"
    api = Api()
    api.add_namespace(log_api)
    api.init_app(app)
    from config import config
    app.config.from_object(config)
    return app


class TestLogApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_log_post_pass(self):
        log_pass = {"application_id": "23457a",
                    "application_log": {
                        "log_timestamp": "2016-07-12 23:13:3",
                        "logging_mode": "INFO",
                        "host_ip": "192.168.1.1",
                        "access_request": "GET",
                        "result_status_code": "200",
                        "user_agent": "mozilla",
                        "user_name": "Gaurav",
                        "bytes_transferred": "12345",
                        "log_message": "hello th@ere"
                    }
                    }
        result_pass = self.test_client.post('/log',
                                            data=json.dumps(log_pass),
                                            content_type='application/json')
        self.assertEqual(result_pass.status_code, 201)

    def test_log_post_fail(self):
        log_pass = {"application_id": "23457a",
                    "application_log": {
                        # "log_timestamp": "2016-07-12 23:13:3",
                        "logging_mode": "INFO",
                        "host_ip": "192.168.1.1",
                        "access_request": "GET",
                        "result_status_code": "200",
                        "user_agent": "mozilla",
                        "user_name": "Gaurav",
                        "bytes_transferred": "12345",
                        "log_message": "hello th@ere"
                    }
                    }
        result_fail = self.test_client.post('/log',
                                            data=json.dumps(log_pass),
                                            content_type='application/json')
        self.assertNotEqual(result_fail.status_code, 201)

    def test_log_get_fail(self):
        response_get = self.test_client.get('/log?log_level=INFO')
        self.assertEqual(response_get.status_code, 400)

    def test_log_get_pass(self):
        response_get = self.test_client.get('/log?application_id=23457')
        self.assertEqual(response_get.status_code, 200)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
