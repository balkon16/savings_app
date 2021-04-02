from collections import OrderedDict

from bson import Decimal128
from bson.json_util import dumps, loads
from pymongo import MongoClient


class Message:

    def __init__(self, status, message):
        assert status is True or status is False
        assert len(message) > 0 and type(message) == str
        self.status = status
        self.message = message

    def __str__(self):
        return 'Status: {}, message: {}'.format(self.status, self.message)

    def __repr__(self):
        return 'Status: {}, message: {}'.format(self.status, self.message)


class MongoConnector:
    # TODO: operacja update na kolekcji
    def __init__(self, host, port, database):
        client = MongoClient(host, port)
        self.db = client[database]

    def drop_collection(self, collection_name):
        self.db.drop_collection(collection_name)
        return Message(True, 'Collection {} dropped'.format(collection_name))

    def create_collection(self, collection_name, **options):
        if collection_name in self.db.list_collection_names():
            # TODO: użyć logging/logger
            return Message(False, 'Collection {} already exists.'.format(collection_name))

        try:
            _ = self.db.create_collection(collection_name)
            msg_text = 'Collection {} created.'.format(collection_name)
            status = True
        except BaseException as exp:
            msg_text = 'Collection not created: {}'.format(exp)
            return Message(False, msg_text)

        if options:
            query = []
            for key, val in options.items():
                query.append((key, val))
            ordered_query = OrderedDict(query)
            # TODO: wyciągnąć status / obsłużyć wyjątek -> przetłumaczyć na Message
            try:
                _ = self.db.command(ordered_query)
                msg_text += ' Command {} executed.'.format(ordered_query)
            except BaseException as exp:
                msg_text += ' Error while executing command: {}'.format(exp)
                status = False
        return Message(status, msg_text)

    def insert(self, collection, payload):
        insert_methods = {dict: 'insert_one', list: 'insert_many'}
        if type(payload) not in insert_methods:
            return Message(False, 'Object of type {} cannot be inserted.'.format(type(payload)))
        method_str = insert_methods.get(type(payload), '')
        obj_method = getattr(self.db[collection], method_str, None)
        try:
            obj_method(payload)
            status = True
            msg_txt = "Insert successful."
        except BaseException as exp:
            status = False
            msg_txt = 'Error while inserting an item: {}'.format(exp)
        return Message(status, msg_txt)

    def delete(self, collection, condition):
        if not isinstance(condition, dict):
            status = False
            msg_text = 'Condition must be a dictionary.'
        else:
            try:
                result = self.db[collection].delete_many(condition)
                status = True
                # TODO: tutaj dać logging.warning
                msg_text = 'Deleted {} documents from collection {}.'.format(collection, result.deleted_count)
            except BaseException as err:
                status = False
                msg_text = "Error while deleting item(s): {}".format(err)
        return Message(status, msg_text)

    def get(self, collection, condition, query_limit=None):
        if not isinstance(condition, dict):
            status = False
            msg_text = 'Condition must be a dictionary.'
        else:
            try:
                result = []
                # TODO: ograć to sprytniej, np. przy pomocy `getattr`
                if query_limit:
                    for doc in self.db[collection].find(condition).limit(query_limit):
                        result.append(doc)
                else:
                    for doc in self.db[collection].find(condition):
                        result.append(doc)
                status = True
                msg_text = dumps(result)
            except BaseException as err:
                status = False
                msg_text = "Error while querying items: {}".format(err)
        return Message(status, msg_text)

    @classmethod
    def parse_content(cls, content):
        return loads(content)

    @classmethod
    def change_type(cls, value, value_type):
        # TODO: mapowanie do konfiguracji
        mapping = {float: {'map_to': Decimal128, "string_first": True}}

        mapped_instr = mapping.get(value_type)
        if not mapped_instr:
            raise NotImplemented('No mapping for {}'.format(value_type))
        if mapped_instr['string_first']:
            value = str(value)
        return mapped_instr['map_to'](value)