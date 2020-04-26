import pymongo
from imsbackend import LOGGER
from bson import ObjectId
import json
from ..config import MONGODB_URL, MONGODB_PORT, MONGODB_DB_NAME


MONGODB_ID = '_id'


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class MongodbRepository(object):

    def __init__(self):
        url = MONGODB_URL
        port = MONGODB_PORT
        db_name = MONGODB_DB_NAME
        self.db_client = self._get_mongodb_objects(url, port, db_name)

    def _get_mongodb_objects(self, url, port, db_name):

        try:
            connection_string = f"mongodb://{url}:" \
                                f"{port}/" \
                                f"{db_name}"

            mongo_client = pymongo.MongoClient(connection_string)
            mongo_db_client = mongo_client[db_name]

        except pymongo.errors.ServerSelectionTimeoutError as err:
            LOGGER.error(f"Connection failed: {err}")
        except pymongo.errors.ConnectionFailure as err:
            LOGGER.error(f"Connection failed: {err}")
        except pymongo.errors.OperationFailure as err:
            LOGGER.error(f"Connection failed: {err}")
        except Exception as excp:
            LOGGER.error(f"Connection failed: {excp}")

        return mongo_db_client

    def str_to_ObjectId(self, identifier):
        """
        :param identifier: identifier to be supplied to mongodb
        :return: '5e928b1eee62036c690c66fd' => ObjectId('5e928b1eee62036c690c66fd')
        """

        id_value = identifier.get(MONGODB_ID)

        if id_value:
            identifier[MONGODB_ID]= ObjectId(id_value)

        return identifier

    def ObjectId_to_str(self, result):
        """
        :param result: MongoDB Result Object {}
        :return: ObjectId('5e928b1eee62036c690c66fd') => '5e928b1eee62036c690c66fd'
        """
        id_value = result.get(MONGODB_ID)

        if id_value:
            result[MONGODB_ID] = MyEncoder().encode(id_value).strip('\"')

        return result

    def find_one(self, collection_name, identifier):
        try:

            identifier = self.str_to_ObjectId(identifier)

            LOGGER.debug(f"collection_name = {collection_name} "
                         f"identifier = {identifier} ")

            collection = self.db_client[collection_name]

            mongodb_result = collection.find_one(identifier)

            LOGGER.debug(f"MONOG: {mongodb_result}")

            if mongodb_result is not None:
                LOGGER.info("find_one: Successful")
                result = self.ObjectId_to_str(mongodb_result)
            else:
                LOGGER.info("find_one: Unsuccessful")
                result = None

        except Exception as excp:
            LOGGER.error(f"exception in find_one: {excp}")
            return None

        LOGGER.debug(f"RESULT: FIND_ONE => {result}")
        return result

    def find_all(self, collection_name, identifier=None):
        try:
            LOGGER.debug(f"collection_name = {collection_name} "
                         f"identifier = {identifier} ")

            collection = self.db_client[collection_name]
            if identifier:
                identifier = self.str_to_ObjectId(identifier)
                mongodb_result = collection.find(identifier)
            else:
                mongodb_result = collection.find()

            if mongodb_result is not None:
                LOGGER.info("find_all: Successful")
                result = [self.ObjectId_to_str(doc) for doc in mongodb_result]
            else:
                LOGGER.info("find_all: Unsuccessful")
                result = []

        except Exception as excp:
            LOGGER.error(f"exception in find_all: {excp}")
            return None

        LOGGER.debug(f"RESULT: FIND_ALL => {result} items retrieved")

        return result

    def insert_one(self, collection_name, insert_dict):
        try:
            LOGGER.debug(f"collection_name = {collection_name} "
                         f"insert_dict = {insert_dict} ")

            collection = self.db_client[collection_name]
            mongodb_result = collection.insert_one(insert_dict)

            if mongodb_result is not None:
                LOGGER.info("insert_one: Successful")
                result = {
                    "acknowledged": mongodb_result.acknowledged,
                    "inserted_id": MyEncoder().encode(mongodb_result.inserted_id).strip('\"')
                }
            else:
                LOGGER.info("insert_one: Unsuccessful")
                result = None

        except Exception as excp:
            LOGGER.error(f"exception in insert_one: {excp}")
            return None

        LOGGER.debug(f"RESULT: INSERT_ONE => {result}")

        return result

    def delete_one(self, collection_name, identifier):
        try:
            identifier = self.str_to_ObjectId(identifier)

            LOGGER.debug(f"collection_name = {collection_name} "
                         f"identifier = {identifier} ")

            collection = self.db_client[collection_name]
            mongodb_result = collection.delete_one(identifier)

            if mongodb_result is not None:
                LOGGER.info("delete_one: Successful")
                result = {
                    "acknowledged": mongodb_result.acknowledged,
                    "deleted_count": mongodb_result.deleted_count,
                    "raw_result": mongodb_result.raw_result
                }
            else:
                LOGGER.info("delete_one: Unsuccessful")
                result = None

        except Exception as excp:
            LOGGER.error(f"exception in delete_one: {excp}")
            return None

        LOGGER.debug(f"RESULT: DELETE_ONE => {result}")
        return result

    def upsert_one(self, collection_name, identifier, new_values):
        """
        identifier = { "address": "Valley 345" }
        new_values = { "$set": { "address": "Canyon 123" } }
        """
        try:
            LOGGER.debug(f"collection_name = {collection_name} "
                         f"identifier = {identifier} "
                         f"new_values = {new_values} ")

            identifier = self.str_to_ObjectId(identifier)
            collection = self.db_client[collection_name]

            mongodb_result = collection.update_one(identifier, new_values, upsert=True)

            if mongodb_result is not None:
                LOGGER.info("upsert_one: Successful")

                result = {
                    "acknowledged": mongodb_result.acknowledged,
                    "matched_count": mongodb_result.matched_count,
                    "modified_count": mongodb_result.modified_count,
                    "raw_result": mongodb_result.raw_result,
                    # upserted_id will be there only when there is no match
                    "upserted_id": self.ObjectId_to_str(mongodb_result.upserted_id)
                }
            else:
                LOGGER.info("upsert_one: Unsuccessful")
                result = None

            LOGGER.info(
                f"update object : modified_count = {result.modified_count}")

        except Exception as excp:
            LOGGER.error(f"Exception in update: {excp}")
            return None

        LOGGER.debug(f"RESULT: UPSERT_ONE => {result}")

        return result

    def count_items(self, collection_name, identifier):
        try:

            LOGGER.debug(f"collection_name = {collection_name} "
                         f"identifier = {identifier} ")

            collection = self.db_client[collection_name]

            mongodb_result = collection.count_documents(identifier)

        except Exception as excp:
            LOGGER.error(f"exception in find_one: {excp}")
            return None

        LOGGER.debug(f"RESULT: COUNT_ITEMS => {mongodb_result}")
        return mongodb_result
