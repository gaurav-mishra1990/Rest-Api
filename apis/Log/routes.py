from flask_restplus import Namespace, Resource
from .parsers import parser, log_parser
from .service import insert_log

api = Namespace('logs', description='Logs related operations')

@api.route('/')
class Log(Resource):
    
    @api.expect(parser)
    @api.expect(log_parser)
    def post(self):
        args = parser.parse_args()
        log_args = log_parser.parse_args(req=args)
        insert_log(args)