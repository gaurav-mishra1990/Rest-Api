from flask_restplus import Namespace, Resource
from flask import jsonify
from datetime import datetime
from apis.Response import Response as Rs

from .parsers import parser, log_parser
from .service import insert_log


def Response_formatter(status_code, hardcoded_message, message):
    # This function formats the response according to the format given.
    # Creates the timestamp and attaches to each response.
    # Then returns the response to the calling function.
    timestamp_creation = datetime.now()
    timestamp_creation = str(timestamp_creation.date()) + \
        " " + str(timestamp_creation.time())
    response_object = Rs(status_code, hardcoded_message, message,
                         timestamp_creation)
    resp = jsonify(response_object.__dict__)
    resp.status_code = status_code
    resp.mimetype = 'application/json'
    return resp


api = Namespace('log', description='Logs related operations')


@api.route('/')
class Log(Resource):
    @api.expect(log_parser)
    @api.expect(parser)
    def post(self):
        args = parser.parse_args(strict=True)
        log_args = log_parser.parse_args(req=args)
        status_code, message = insert_log(args)
        if status_code == 201:
            hardcoded_message = "LOG_POSTED_SUCCESSFULLY"
        else:
            hardcoded_message = "LOG_NOT_POSTED"

        return Response_formatter(status_code, hardcoded_message, message)
