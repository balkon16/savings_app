import json
from pymongo import MongoClient

with open('./configuration/app_configuration.json', 'r') as f:
    mongo_conf = json.load(f)['mongodb']


class MongoConnector:

    def __init__(self, host, port):
        self.client = MongoClient(mongo_conf['host'], mongo_conf['port'])

    # TODO: wyszukiwanie elementów -> find; metoda ma zwracać {"success": T/F, "data": ...}
    # TODO: wstawianie elementów (insert, update, upsert); metoda ma informować czy udał się zapis
    # TODO: usuwanie elementów; metoda ma informować czy ok
    # TODO: tworzenie kolekcji (jeżeli już istnieje wyjątek); komunikat czy ok
    # TODO: tworzenie bazy (jeżeli już jest wyjątek); komunikat czy ok
