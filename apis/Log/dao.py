import os
import json
from datetime import datetime


storage_type = os.getenv("STORAGE_TYPE")
es_host = os.getenv("ES_HOST")
es_port = os.getenv("ES_PORT")


def date_converter(datetime_object):
    return datetime_object.__str__()


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': es_host, 'port': es_port}])
    if _es.ping():
        return True
    else:
        return False


def insert_in_es(log):
    from elasticsearch import Elasticsearch




def insert_db(log):
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

    log_object = Application_Log(application_id=application_id, application_name=application_name, application_type=application_type, log_timestamp=log_timestamp, log_message=log_message,logging_mode=logging_mode, host_ip=host_ip, access_request=access_request,result_status_code=result_status_code, user_agent=user_agent, user_name=user_name,bytes_transferred=bytes_transferred)

    db.session.add(log_object)
    db.session.commit()
    db.session.close()



def insert_log_in_db(log):
    es_connected = True
    # es_connected = connect_elasticsearch()
    if es_connected:
        if storage_type == 'file_storage':
            log_file = os.getenv("LOG_FILE")
            try:
                f = open(log_file, 'a')
                insert_in_es(log)
            except IOError:
                print("Could not open file")
            
            with f:
                log['timestamp'] = datetime.utcnow()
                del log["unparsed_arguments"]
                log_str = json.dumps(log, default = date_converter, indent=4)
                f.write('{},\n'.format(log_str))
                f.close()

        elif storage_type == 'database':
            insert_db(log)
        else:
            pass
    else:
        pass
    
    # if storage_type == 'file_storage':
    #     file = os.getenv("FILE")
    #     with open(file, 'a') as f:
    #         f.write("hello")
            


        

