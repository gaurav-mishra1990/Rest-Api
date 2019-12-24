from flask_restplus import Namespace, Resource
from flask import jsonify, request
from datetime import datetime
from apis.Response import Response as Rs

from .parsers import parser, log_parser
from .service import insert_log, get_log


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


@api.route('')
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

    def get(self):
        request_dict = {
            "application_id": None,
            "log_level": None,
            "status_code": None,
            "date": None
        }
        application_id = request.args.get("application_id")
        if not application_id:
            return Response_formatter(400, "NO_APPLICATION_ID", "No Application Id passed in the request")
        else:
            request_dict["application_id"] = application_id
            request_dict["log_level"] = request.args.get("log_level")
            request_dict["status_code"] = request.args.get("status_code")
            request_dict["date"] = request.args.get("date")
            status_code, response_message = get_log(request_dict)

        if status_code == 200:
            hardcoded_message = "SUCCESSFUL_GET_REQUEST"
        else:
            hardcoded_message = "NO_RESPONSE_FOR_GET_REQUEST"

        return Response_formatter(status_code, hardcoded_message, response_message)
