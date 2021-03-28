import datetime
import json
import os

from flask import Flask, request
from werkzeug.utils import secure_filename

from mongo.mongodb_connector import MongoConnector

# TODO: do konfiguracji
UPLOAD_FOLDER = './uploaded_files'

with open('./configuration/app_configuration.json', 'r') as f:
    conf = json.load(f)
    mongo_conf = conf['mongodb']
    file_upload_conf = conf['file_upload']

ALLOWED_EXTENSIONS = file_upload_conf['allowed_extensions']
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
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# TODO: endpoint do pobrania kursów historycznych -> GET

# TODO: wzorzec pliki do załadowania (xlsx, xls)

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


@app.route('/currencies', methods=['PUT'])
def add_currency_pair():
    # TODO: dokumentacja -> wymagany `Content-Type: application/json` w requeście
    # TODO: dokumentacja -> wymagany odpowiedni format daty datetime.datetime.now()
    data_json = request.json
    insert_data = dict()
    # TODO: przygotować metodę w MongoConnector, która odpowiednio przygotuje dane
    for key, value in data_json.items():
        if type(value) is float:
            insert_data[key] = MongoConnector.change_type(value, float)
        else:
            insert_data[key] = value
    insert_data['timestamp'] = datetime.datetime.now()
    res_msg = mongo_connector.insert(EXCHANGE_RATES_COLLECTION_NAME, insert_data)
    if res_msg.status:
        return res_msg.message, 200
    else:
        return res_msg.message, 400


@app.route('/assets', methods=['GET', 'PUT'])
def handle_assets():
    if request.method == 'GET':
        res_msg = mongo_connector.get(ASSETS_COLLECTION_NAME, {})
        # TODO: konwersja Decimal128 na float -> klasa Converter
        if res_msg.status:
            return res_msg.message, 200
        return res_msg, 400
    elif request.method == 'PUT':
        data_json = request.json
        insert_data = dict()
        for key, value in data_json.items():
            if type(value) is float:
                insert_data[key] = MongoConnector.change_type(value, float)
            else:
                insert_data[key] = value
        insert_data['timestamp'] = datetime.datetime.now()
        res_msg = mongo_connector.insert(ASSETS_COLLECTION_NAME, insert_data)
        if res_msg.status:
            return res_msg.message, 200
        else:
            return res_msg.message, 400
    else:
        return 501, 'Method {} is not implemented'.format(request.method)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file', 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File saved', 200
    return "Incorrect file type", 400


if __name__ == '__main__':
    app.run(debug=True)
