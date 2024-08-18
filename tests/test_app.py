import pytest
from app.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_valid_order_TWD(client):
    order_data = {
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": "1000",
        "currency": "TWD"
    }
    response = client.post('/api/orders', json=order_data)
    response_json = response.get_json()

    assert response.status_code == 200
    assert response_json['status_code'] == 200
    assert response_json['message'] == "Valid order"
    assert response_json['data'] == order_data


def test_valid_order_USD(client):
    order_data = {
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": "10",
        "currency": "USD"
    }
    process_data = {
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": "310",
        "currency": "TWD"
    }
    response = client.post('/api/orders', json=order_data)
    response_json = response.get_json()

    assert response.status_code == 200
    assert response_json['status_code'] == 200
    assert response_json['message'] == "Valid order"
    assert response_json['data'] == process_data


def test_invalid_json_format_1(client):
    order_data = {
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        # Missing address
        "price": "310",
        "currency": "TWD"
    }
    response = client.post('/api/orders', json=order_data)
    response_json = response.get_json()

    assert response.status_code == 400
    assert response_json['status_code'] == 400
    assert response_json['message'] == "JSON format is incorrect"
    assert response_json['data'] == order_data


def test_invalid_json_format(client):
    order_data = {
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": "A10",
        "currency": "USD"
    }
    response = client.post('/api/orders', json=order_data)
    response_json = response.get_json()

    assert response.status_code == 400
    assert response_json['status_code'] == 400
    assert response_json['message'] == "JSON format is incorrect"
    assert response_json['data'] == order_data


def test_invalid_name_format_1(client):
    order_data = {
        "id": "A0000001",
        "name": "Mel123ody holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": "3000",
        "currency": "TWD"
    }
    response = client.post('/api/orders', json=order_data)
    response_json = response.get_json()

    assert response.status_code == 400
    assert response_json['status_code'] == 400
    assert response_json['message'] == "Name contains non-English characters"
    assert response_json['data'] == order_data


def test_invalid_name_format_2(client):
    order_data = {
        "id": "A0000001",
        "name": "Melody holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": "3000",
        "currency": "TWD"
    }
    response = client.post('/api/orders', json=order_data)
    response_json = response.get_json()

    assert response.status_code == 400
    assert response_json['status_code'] == 400
    assert response_json['message'] == "Name is not capitalized"
    assert response_json['data'] == order_data


def test_invalid_price_1(client):
    order_data = {
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": "3000",
        "currency": "TWD"
    }
    response = client.post('/api/orders', json=order_data)
    response_json = response.get_json()

    assert response.status_code == 400
    assert response_json['status_code'] == 400
    assert response_json['message'] == "Price is over 2000"
    assert response_json['data'] == order_data


def test_invalid_price_2(client):
    order_data = {
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": "200",
        "currency": "USD"
    }

    process_data = {
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": "6200",
        "currency": "TWD"
    }

    response = client.post('/api/orders', json=order_data)
    response_json = response.get_json()

    assert response.status_code == 400
    assert response_json['status_code'] == 400
    assert response_json['message'] == "Price is over 2000"
    assert response_json['data'] == process_data


def test_invalid_currency(client):
    order_data = {
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": "1000",
        "currency": "EUR"
    }
    response = client.post('/api/orders', json=order_data)
    response_json = response.get_json()

    assert response.status_code == 400
    assert response_json['status_code'] == 400
    assert response_json['message'] == "Currency format is wrong"
    assert response_json['data'] == order_data
