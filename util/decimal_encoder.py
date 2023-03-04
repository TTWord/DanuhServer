import json
import decimal

class Encoder(json.JSONEncoder):
    @staticmethod
    def default(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
