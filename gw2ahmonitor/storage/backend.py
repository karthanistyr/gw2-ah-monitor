from abc import ABCMeta, abstractmethod
import pymongo

class BackendBase:

    @abstractmethod
    def insert(self, table_name, items):
        pass

    def upsert(self, table_name, items):
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

        #TODO: hacky, improve this
        #ensure indexes
        self.db["item"].create_index(keys=[("id", pymongo.ASCENDING)])
        self.db["item_error"].create_index(keys=[("id", pymongo.ASCENDING)])
        self.db["price_point"].create_index(keys=[("id", pymongo.ASCENDING)])
        self.db["price_point_error"].create_index(keys=[("id", pymongo.ASCENDING)])
        self.db["listing"].create_index(keys=[("id", pymongo.ASCENDING)])
        self.db["listing_error"].create_index(keys=[("id", pymongo.ASCENDING)])

    def insert(self, table_name, items):
        return self.db[table_name].insert_many(items)

    def upsert(self, table_name, items):
        # prepare upsert operations
        upserts = []
        for item in items:
            upserts.append(pymongo.operations.ReplaceOne(
                filter={"id": item["id"]},
                replacement=item,
                upsert=True
                ))
        return self.db[table_name].bulk_write(upserts)

    def get(self, table_name, predicate):
        return self.db[table_name].find(predicate)
