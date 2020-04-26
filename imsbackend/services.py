from imsbackend.repository import Repository
from imsbackend.repository.mongo import MongodbRepository
from imsbackend.schema import BranchSchema
from imsbackend import LOGGER


class Service(object):
    def __init__(self, repo_client=Repository(adapter=MongodbRepository)):
        self.db_client = repo_client
        # self.user_id = user_id
        #
        # if not user_id:
        #     raise Exception("user id not provided")

    def find_one(self, collection, selector):
        return self.db_client.find_one(collection, selector)

    def find_all(self, collection, selector):
        return self.db_client.find_all(collection, selector)

    def insert_one(self, collection, selector):
        return self.db_client.insert_one(collection, selector)

    def delete_one(self, col, identifier):
        return self.db_client.delete_one(col, identifier)

    def upsert_one(self, col, identifier, new_values):
        return self.db_client.upsert_one(col, identifier, new_values)

    def count_items(self, collection, selector):
        return self.db_client.count_items(collection, selector)

    def close(self):
        return self.db_client.close()

    # def dump(self, data):
    #     try:
    #         result = BranchSchema().dump(data)
    #         # LOGGER.info(result)
    #     except Exception as excp:
    #         LOGGER.error(f"Schema error: {excp}")
    #         return None
    #     return result
