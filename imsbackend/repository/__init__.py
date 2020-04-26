import json


class Repository(object):
    def __init__(self, adapter=None):
        self.client = adapter()

    def find_one(self, col, identifier):
        result = self.client.find_one(col, identifier)
        return result

    def find_all(self, col, identifier):
        return self.client.find_all(col, identifier)

    def insert_one(self, col, data_dict):
        return self.client.insert_one(col, data_dict)

    def delete_one(self, col, identifier):
        return self.client.delete_one(col, identifier)

    def upsert_one(self, col, identifier, new_values):
        return self.client.upsert_one(col, identifier, new_values)

    def count_items(self, col, identifier):
        result = self.client.count_items(col, identifier)
        return result

    def close(self):
        return self.client.close()
