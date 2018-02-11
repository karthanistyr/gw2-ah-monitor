from abc import ABCMeta, abstractmethod
import pymongo

class BackendBase:

    @abstractmethod
    def insert(self, table_name, items):
        pass

    @abstractmethod
    def get(self, table_name, predicate):
        pass

class MongoDbBackend(BackendBase):
    mongodb_hostname = "localhost"
    mongodb_port = 27017
    mongodb_db_name = "gw2-ah-monitor"

    def __init__(self):
        # TODO test availability of mongodb service
        client = pymongo.MongoClient(MongoDbBackend.mongodb_hostname,
            MongoDbBackend.mongodb_port)
        self.db = client.get_database(name=MongoDbBackend.mongodb_db_name)

    def insert(self, table_name, items):
        return self.db[table_name].insert_many(items)

    def get(self, table_name, predicate):
        return self.db[table_name].find(predicate)
