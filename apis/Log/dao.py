from elasticsearch import Elasticsearch
import os
import json

storage_type = os.getenv("STORAGE_TYPE")
es_host = os.getenv("ES_HOST")
es_port = os.getenv("ES_PORT")


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': es_host, 'port': es_port}])
    if _es.ping():
        return True
    else:
        return False
    return _es


def insert_log_in_db(log):
    es_connected = True
    if es_connected:
        if storage_type == 'file_storage':
            log_file = os.getenv("LOG_FILE")
            try:
                f = open(log_file, 'a')
            except IOError:
                print("Could not open file")
            
            with f:
                del log["unparsed_arguments"]
                log_str = json.dumps(log, indent=4)
                f.write('{},\n'.format(log_str))
                f.close()
    else:
        pass
    
    # if storage_type == 'file_storage':
    #     file = os.getenv("FILE")
    #     with open(file, 'a') as f:
    #         f.write("hello")
            


        

