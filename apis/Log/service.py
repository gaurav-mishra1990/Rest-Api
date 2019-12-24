from .dao import store_log, get_logs_from_db


def insert_log(log):
    return store_log(log)


def get_log(args):
    return get_logs_from_db(args)
