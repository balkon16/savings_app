# TODO: zrobić z tego testy jednostkowe

import json
from bson.decimal128 import Decimal128
import datetime
from mongo.mongodb_connector import MongoConnector

COLLECTION_NAME = 'test_asset_collection'

with open('./schemas/asset_schema.json') as f:
    asset_schema = json.load(f)

mc = MongoConnector('localhost', 27017, 'test_db')
validator = {"$jsonSchema": asset_schema}
mc.drop_collection(COLLECTION_NAME)
mc.create_collection(COLLECTION_NAME, collMod=COLLECTION_NAME, validator=validator)

item = {
    "name": "Asset no 1",
    "entity": "Bank no 1",
    "tags": ['abc', 'def'],
    "ticker": "ANO",
    "currency": "RUB",
    "value": Decimal128("123.31"),
    "timestamp": datetime.datetime.now()
}
msg = mc.insert(COLLECTION_NAME, item)
print(msg)
