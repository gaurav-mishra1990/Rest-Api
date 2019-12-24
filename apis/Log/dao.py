import os
import json
from datetime import datetime
from elasticsearch import Elasticsearch


storage_type = os.getenv("STORAGE_TYPE")
es_host = os.getenv("ES_HOST")
es_port = os.getenv("ES_PORT")


def date_converter(datetime_object):
    return datetime_object.__str__()


def date_formatter(datetime_object):
    year = datetime_object.year
    month = datetime_object.month
    day = datetime_object.day
    hour = datetime_object.hour
    minute = datetime_object.minute
    second = datetime_object.second
    timestamp = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    return timestamp


def form_log_dict(log_json):
    log = dict()
    log['application_id'] = log_json["application_id"]
    application_log = log_json["application_log"]
    log['timestamp'] = log_json["timestamp"]

    keys = application_log.keys()

    log['application_name'] = log_json["application_name"] if "application_name" in log_json.keys() else None
    log['application_type'] = log_json["application_type"] if "application_type" in log_json.keys() else None
    application_log['logging_mode'] = application_log["logging_mode"] if "logging_mode" in keys else None
    application_log['host_ip'] = application_log["host_ip"] if "host_ip" in keys else None
    application_log['access_request'] = application_log["access_request"] if "access_request" in keys else None
    application_log['result_status_code'] = application_log["result_status_code"] if "result_status_code" in keys else None
    application_log['user_agent'] = application_log["user_agent"] if "user_agent" in keys else None
    application_log['user_name'] = application_log["user_name"] if "user_name" in keys else None
    application_log['bytes_transferred'] = application_log["bytes_transferred"] if "bytes_transferred" in keys else None
    log["application_log"] = application_log

    return log


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': es_host, 'port': es_port}])
    if _es.ping():
        print("Connected to Elasticsearch server")
    else:
        print("Not able to connect to Elasticsearch server")
    return _es


def insert_in_es(elastic_object, index_name, record):
    try:
        temp = elastic_object.index(index=index_name, doc_type='_doc', body=record)
        return True
    except Exception:
        return False


def insert_in_db(log):
    from models import Application_Log
    from app import db

    application_id = log["application_id"]
    application_log = log["application_log"]
    log_timestamp = application_log["log_timestamp"]
    log_message = application_log["log_message"]

    keys = application_log.keys()

    application_name = log["application_name"] if "application_name" in log.keys() else None
    application_type = log["application_type"] if "application_type" in log.keys() else None
    logging_mode = application_log["logging_mode"] if "logging_mode" in keys else None
    host_ip = application_log["host_ip"] if "host_ip" in keys else None
    access_request = application_log["access_request"] if "access_request" in keys else None
    result_status_code = application_log["result_status_code"] if "result_status_code" in keys else None
    user_agent = application_log["user_agent"] if "user_agent" in keys else None
    user_name = application_log["user_name"] if "user_name" in keys else None
    bytes_transferred = application_log["bytes_transferred"] if "bytes_transferred" in keys else None

    log_object = Application_Log(application_id=application_id, application_name=application_name, application_type=application_type, log_timestamp=log_timestamp, log_message=log_message, logging_mode=logging_mode, host_ip=host_ip, access_request=access_request, result_status_code=result_status_code, user_agent=user_agent, user_name=user_name, bytes_transferred=bytes_transferred)

    try:
        db.session.add(log_object)
        db.session.commit()
        db.session.close()
        return True
    except Exception:
        return False


def store_log(log_json):
    es = connect_elasticsearch()
    log_json['timestamp'] = date_formatter(datetime.utcnow())
    if es is not None:
        if storage_type == 'file_storage':
            log_file = os.getenv("LOG_FILE")
            try:
                f = open(log_file, 'a')
                del log_json["unparsed_arguments"]
                log_str = json.dumps(log_json, default=date_converter, indent=4)
                log = form_log_dict(log_json)
                flag = insert_in_es(es, index_name="logs", record=log)
                if not flag:
                    return (500, "Internal Server Error")
            except IOError:
                return (500, "Internal Server Error")
            with f:
                f.write('{},\n'.format(log_str))
                f.close()
                return (201, "Resource Posted Successfully")

        elif storage_type == 'database':
            del log_json["unparsed_arguments"]
            log = form_log_dict(log_json)
            flag = insert_in_es(es, index_name="logs", record=log)
            if flag:
                flag_db = insert_in_db(log_json)
                if flag_db:
                    return (201, "Resource Posted Successfully")
                else:
                    return (500, "Internal Server Error")
            else:
                return (500, "Internal Server Error")
        else:
            pass
    else:
        return (500, "Internal Server Error")


def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)
    return res


def get_logs_from_db(args):
    es = connect_elasticsearch()
    if es is not None:
        search_object = {'query': {'match': {'application_id': args['application_id']}}}
        query_result = search(es, 'logs', json.dumps(search_object))

        results = list()

        for log_temp in query_result['hits']['hits']:
            log = log_temp['_source']
                
            if "timestamp" in log.keys():
                del log["timestamp"]

            log_date = log['application_log']['log_timestamp'].split(" ")[0]

            if (args["log_level"] == log['application_log']["logging_mode"] or (not args["log_level"])) and (args["status_code"] == log['application_log']["result_status_code"] or (not args['status_code'])) and (args["date"] == log_date or (not args["date"])):
                results.append(log)

        return results