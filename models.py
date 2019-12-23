from app import db
from datetime import datetime


class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True)
    application_name = db.Column(db.String(64), index=True, nullable=False)
    application_type = db.Column(db.String(64), index=True)


class Application_Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    logging_mode = db.Column(db.String(64), index=True)
    host_ip = db.Column(db.String(64))
    access_request = db.Column(db.String(64), index=True)
    result_status_code = db.Column(db.Integer, index=True)
    user_agent = db.Column(db.String(64))
    user_name = db.Column(db.String(64))
    bytes_transferred = db.Column(db.BigInteger)
    log_message = db.Column(db.String(250))

    def __init__(self, application_id, timestamp, logging_mode, host_ip, access_request, result_status_code, user_agent, user_name, bytes_transferred, log_message):
        
        self.application_id = application_id
        self.timestamp = timestamp
        self.logging_mode = logging_mode
        self.host_ip = host_ip
        self.access_request = access_request
        self.result_status_code = result_status_code
        self.user_agent = user_agent
        self.user_name = user_name
        self.bytes_transferred = bytes_transferred
        self.log_message = log_message
    