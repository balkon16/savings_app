import json

from flask import Flask, request

from mongo.mongodb_connector import MongoConnector

with open('./configuration/app_configuration.json', 'r') as f:
    mongo_conf = json.load(f)['mongodb']

ASSETS_COLLECTION_NAME = mongo_conf['db_info']['collections']['assets_collection']
EXCHANGE_RATES_COLLECTION_NAME = mongo_conf['db_info']['collections']['exchange_rates_collection']

mongo_connector = MongoConnector(mongo_conf['host'],
                                 mongo_conf['port'],
                                 mongo_conf['db_info']['name'])

# TODO: testy metod API -> jak je przeprowadzić?
# TODO: skrypt robiący backup danych MongoDB
# TODO: logging (jak w pracy)
# TODO: plik konfiguracyjny, w którym będą wszystkie ścieżki

# TODO: mapowanie typów mongo na Pythonowe, żeby poradzić sobie z problemami tego typu : "multiplier": {"$numberDecimal": "4.51"}, "source": "NBP", "timestamp": {"$date": 1602586433000}}
#  > sprawdzić tap-mongodb

app = Flask(__name__)


# TODO: endpoint dla nowych kursów -> PUT
# TODO: endpoint dla nowych aktywów -> PUT
# TODO: endpoint do pobrania kursów historycznych -> GET
# TODO: endpoint do pobrania aktywów: ticker, tag(s), currency -> GET

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/currencies', methods=['GET'])
def get_exchange_rate():
    # TODO: wprowadzić obsługę timestamp (na razie zwracam najnowszy kurs z bazy)
    def _check_string(string):
        if not string.isupper() or len(string) != 3:
            return False
        return True

    base = request.args.get('base')
    quote = request.args.get('quote')
    if not base or not quote:
        return 'There must be two currencies provided', 400

    if _check_string(base) and _check_string(quote):
        condition = {"$query": {"base_currency": base, "quote_currency": quote},
                     "$orderby": {"timestamp": -1}}
        result_msg = mongo_connector.get(EXCHANGE_RATES_COLLECTION_NAME, condition, 1)
        if result_msg.status:
            result_content = mongo_connector.parse_content(result_msg.message)
            if len(result_content) == 0:
                return 'Pair {}/{} not found'.format(base, quote), 404
            else:
                value = result_content[0]['value']
                mult = result_content[0]['multiplier']
                result = float(value.to_decimal() / mult.to_decimal())
                return {"value": result}, 200
        else:
            return result_msg.message, 400
    else:
        return 'Currency code must be a 3-element string written in upper case.', 400

if __name__ == '__main__':
    app.run(debug=True)
