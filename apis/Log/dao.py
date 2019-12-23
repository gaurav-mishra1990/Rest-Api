from elasticsearch import Elasticsearch

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        return True
    else:
        return False
    return _es


def insert_log_in_db():
    es_connected = connect_elasticsearch()
    if es_connected:
        pass
    else:
        pass
        

