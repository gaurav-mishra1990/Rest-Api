from elasticsearch import Elasticsearch

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        # print('Yay Connect')
        pass
    else:
        # print('Awww it could not connect!')
        pass
    return _es


def test():
    temp = connect_elasticsearch()
    print(temp)
