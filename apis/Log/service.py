from .dao import store_log


def insert_log(log):
    return store_log(log)
