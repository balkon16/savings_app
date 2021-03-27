from flask import Flask

from mongo.mongodb_connector import MongoConnector

# mongo_connector = MongoConnector()

# TODO: testy metod API -> jak je przeprowadzić?
# TODO: skrypt robiący backup danych MongoDB
# TODO: logging (jak w pracy)
# TODO: plik konfiguracyjny, w którym będą wszystkie ścieżki

# TODO: mapowanie typów mongo na Pythonowe, żeby poradzić sobie z problemami tego typu : "multiplier": {"$numberDecimal": "4.51"}, "source": "NBP", "timestamp": {"$date": 1602586433000}}
#  > sprawdzić tap-mongodb

app = Flask(__name__)
api = Api(app)


# TODO: zwykły falsk
# TODO: endpoint dla nowych kursów -> PUT
# TODO: endpoint dla nowych aktywów -> PUT
# TODO: endpoint do pobierania najnowszego kursu -> GET
# TODO: endpoint do pobrania kursów historycznych -> GET
# TODO: endpoint do pobrania aktywów: ticker, tag(s), currency -> GET

# class Asset(Resource):
#     pass

#
# class ExchangeRate(Resource):
#     def get(self, base_currency, quote_currency):
#         def _check_string(string):
#             if not string.isupper() or len(string) != 3:
#                 return False
#             return True
#         if _check_string(base_currency) and _check_string(quote_currency):
#             return 200, {"value": 3.40}
#         else:
#             return 400, 'Currency code must be a 3-element string written in upper case.'


# api.add_resource(ExchangeRate, '/')

if __name__ == '__main__':
    app.run(debug=True)
