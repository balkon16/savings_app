import json
from collections import OrderedDict

import pymongo
from pymongo import MongoClient

with open('./configuration/app_configuration.json', 'r') as f:
    mongo_conf = json.load(f)['mongodb']


# TODO: currency_pairs_schema.json -> walidacja (`source` nie może być pusty) + odpowiedni opis w description
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

    def __init__(self, host, port, database):
        client = MongoClient(host, port)
        self.db = client[database]

    def drop_collection(self, collection_name):
        self.db.drop_collection(collection_name)
        return Message(True, 'ok')

    def create_collection(self, collection_name, **options):
        if collection_name in self.db.list_collection_names():
            # TODO: użyć logging/logger
            return Message(False, 'Collection {} already exists.'.format(collection_name))

        # TODO: uwspólnić obsługę wyjątków
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

    # TODO: wyszukiwanie elementów -> find; metoda ma zwracać {"success": T/F, "data": ...}
    # TODO: wstawianie elementów (insert, update, upsert); metoda ma informować czy udał się zapis
    # TODO: usuwanie elementów; metoda ma informować czy ok
