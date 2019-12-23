from elasticsearch import Elasticsearch
import os

storage_type = os.getenv("STORAGE_TYPE")


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        return True
    else:
        return False
    return _es


def insert_log_in_db(log):
    # es_connected = connect_elasticsearch()
    # if es_connected:
    #     pass
    # else:
    #     pass
    if storage_type == 'file_storage':
        file = os.getenv("FILE")
        with open(file, 'a') as f:
            f.write("hello")
            


        

