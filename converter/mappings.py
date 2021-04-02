from bson import Decimal128

PYTHON_TO_MONGO = {float: {'map_to': Decimal128, "string_first": True}}
MONGO_TO_PYTHON = dict()
