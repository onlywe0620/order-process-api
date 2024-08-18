from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError


app = Flask(__name__)


class FormValidation:

    def __init__(self):
        self.schema = {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "address": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "district": {"type": "string"},
                        "street": {"type": "string"}
                    },
                    "required": ["city", "district", "street"]
                },
                "price": {
                    "type": "string",
                    "pattern": "^[0-9]+$"
                },
                "currency": {"type": "string"}
            },
            "required": ["id", "name", "address", "price", "currency"]
        }

    def validate_schema_format(self, data):
        try:
            validate(instance=data, schema=self.schema)
            return True
        except ValidationError:
            return False


class FormatCheckingAndTransform:
    EXCHANGE_RATE = 31

    def check_and_transform(self, order_data):
        if not all(c.isalpha() or c.isspace() for c in order_data['name']):
            raise ValueError("Name contains non-English characters")

        words = order_data['name'].split()
        if not all(word[0].isupper() for word in words):
            raise ValueError("Name is not capitalized")

        if order_data['currency'] not in ['TWD', 'USD']:
            raise ValueError("Currency format is wrong")

        price = int(order_data['price'])
        if order_data['currency'] == 'USD':
            price *= self.EXCHANGE_RATE
            order_data['price'] = str(price)
            order_data['currency'] = 'TWD'

        if price > 2000:
            raise ValueError("Price is over 2000")

        return order_data


class Service:
    def __init__(self, format_checker):
        self.format_checker = format_checker

    def process_order(self, order_data):
        return self.format_checker.check_and_transform(order_data)


class Response:
    def __init__(self, status_code, data, message):
        self.status_code = status_code
        self.data = data
        self.message = message

    def send(self):
        return {
            'status_code': self.status_code,
            'data': self.data,
            'message': self.message
        }


@app.route('/api/orders', methods=['POST'])
def api_orders():
    try:
        form_validator = FormValidation()
        format_checker = FormatCheckingAndTransform()
        service = Service(format_checker)

        order_data = request.json
        format_vaild = form_validator.validate_schema_format(order_data)
        if format_vaild:
            processed_data = service.process_order(order_data)
            response = Response(200, processed_data, 'Valid order')
        else:
            response = Response(400, order_data, "JSON format is incorrect")
        return jsonify(response.send()), response.send()['status_code']
    except ValueError as e:
        response = Response(400, order_data, str(e))
        return jsonify(response.send()), response.send()['status_code']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
