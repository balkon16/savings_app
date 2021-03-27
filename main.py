from flask import Flask
from flask_restful import Resource, Api

from mongo.mongodb_connector import MongoConnector
# TODO: testy metod API -> jak je przeprowadzić?
# TODO: skrypt robiący backup danych MongoDB
# TODO: przygotować schematy danych pod kątem walidacji przy insert do MongoDB (https://docs.mongodb.com/manual/core/schema-validation/)
# TODO: logging (jak w pracy)
# TODO: plik konfiguracyjny, w którym będą wszystkie ścieżki

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)