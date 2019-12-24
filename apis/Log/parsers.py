# Parsing the arguments for the incoming post request for logs.

from flask_restplus import reqparse, inputs
from datetime import datetime

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('application_id', type=str, required=True, help='No application id given or id not valid.')
parser.add_argument('application_type', type=str)
parser.add_argument('application_name', type=str)
parser.add_argument('application_log', type=dict, required=True, help='No log provided.')

log_parser = reqparse.RequestParser()
log_parser.add_argument('log_timestamp', required=True, type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), location=('application_log'), help='No timestamp provided for the log or wrong format.')
log_parser.add_argument('logging_mode', type=str, location=('application_log'))
log_parser.add_argument('host_ip', type=inputs.ip, location=('application_log'))
log_parser.add_argument('access_request', type=str, location=('application_log'))
log_parser.add_argument('result_status_code', type=int, location=('application_log'))
log_parser.add_argument('user_agent', type=str, location=('application_log'))
log_parser.add_argument('user_name', type=str, location=('application_log'))
log_parser.add_argument('bytes_transferred', type=int, location=('application_log'))
log_parser.add_argument('log_message', type=str, required=True, location=('application_log'))
