from app import db
from datetime import datetime


class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True)
    application_name = db.Column(db.String(64), index=True, nullable=False)
    application_type = db.Column(db.String(64), index=True)


class Application_Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey(Application.application_id), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    logging_mode = db.Column(db.String(64), index=True)
    host_ip = db.Column(db.String(64))
    access_request = db.Column(db.String(64), index=True)
    application_type = db.Column(db.String(64), index=True)
    result_status_code = db.Column(db.Integer, index=True)
    user_agent = db.Column(db.String(64))
    user_name = db.Column(db.String(64))
    bytes_transferred = db.Column(db.BigInteger)
    log_message = db.Column(db.String(250))
    