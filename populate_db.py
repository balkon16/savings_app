import json
from bson.decimal128 import Decimal128
import datetime

from mongo.mongodb_connector import MongoConnector

dts_now = datetime.datetime.now()
dts_past = datetime.datetime.now() - datetime.timedelta(days=14)

all_items = {
    "assets": [
        {"name": "Asset no 1",
         "entity": "Bank no 1",
         "tags": ['tag_test1', 'tag_test2'],
         "ticker": "ANO",
         "currency": "EUR",
         "value": Decimal128("123.31"),
         "timestamp": datetime.datetime.now()}
    ],
    "exchange_rates": [
        {"base_currency": "EUR",
         "quote_currency": "PLN",
         "multiplier": Decimal128("1.0"),
         "value": Decimal128("4.51"),
         "source": "NBP",
         "timestamp": dts_now},
        {"base_currency": "EUR",
         "quote_currency": "PLN",
         "multiplier": Decimal128("1.0"),
         "value": Decimal128("4.30"),
         "source": "NBP",
         "timestamp": dts_past},
        {"base_currency": "USD",
         "quote_currency": "PLN",
         "multiplier": Decimal128("1.0"),
         "value": Decimal128("3.78"),
         "source": "NBP",
         "timestamp": dts_past},
        {"base_currency": "CHF",
         "quote_currency": "PLN",
         "multiplier": Decimal128("1.0"),
         "value": Decimal128("4.15"),
         "source": "",
         "timestamp": dts_past}
    ]
}

with open('./configuration/app_configuration.json', 'r') as f:
    mongo_conf = json.load(f)['mongodb']

mongo_connector = MongoConnector(mongo_conf['host'],
                                 mongo_conf['port'],
                                 mongo_conf['db_info']['name'])

for collection_obj, collection_name in mongo_conf['db_info']['collections'].items():
    entity = collection_obj.replace('_collection', '')
    schema_file_name = './mongo/schemas/{}_schema.json'.format(entity)
    with open(schema_file_name, 'r') as f:
        schema = json.load(f)
    mongo_connector.drop_collection(collection_name)
    mongo_connector.create_collection(collection_name,
                                      collMod=collection_name,
                                      validator={"$jsonSchema": schema})
    mongo_connector.insert(collection_name, all_items[entity])
