import requests
import json
import pytest
import random

site = "http://192.168.1.23:5000/"


def test_UserRegister():
    url = "api/users/register"
    Input = {
        "card_info": "cardInformation",
        "email": "email@gmail.com",
        "phone_num": "5321234567",
        "username": "username"
    }

    requestJson = json.dumps(Input, indent=4)
    requestJson = json.loads(requestJson)

    response = requests.post(site + url, json=requestJson)

    assert response.status_code == 200


def test_UserEdit():
    url = "api/user/update"
    Input = {
        "card_info": "cardInformation",
        "email": "emailEdited@gmail.com",
        "phone_num": "5327654321",
        "username": "selin"
    }

    requestJson = json.dumps(Input, indent=4)
    requestJson = json.loads(requestJson)
    response = requests.post(site + url, json=requestJson)

    assert response.status_code == 200


def test_GetByCardInformation():
    url = "api/user"
    Input = {
        "card_info": "cardInformation"
    }

    requestJson = json.dumps(Input, indent=4)
    requestJson = json.loads(requestJson)
    response = requests.post(site + url, json=requestJson)

    assert response.status_code == 200


def test_cardParkPriceAdd():
    url = "api/prices/add"
    Input = {
        "minutes": 90,
        "price": 150
    }

    requestJson = json.dumps(Input, indent=4)
    requestJson = json.loads(requestJson)
    response = requests.post(site + url, json=requestJson)

    assert response.status_code == 200


def test_cardParkPriceUpdate():
    url = "api/prices/update"
    Input = {
        "minutes": 90,
        "price": 160
    }

    requestJson = json.dumps(Input, indent=4)
    requestJson = json.loads(requestJson)
    response = requests.post(site + url, json=requestJson)

    assert response.status_code == 200


def test_cardParkPricedelete():
    url = "api/prices/delete"
    Input = {
        "minutes": 90
    }

    requestJson = json.dumps(Input, indent=4)
    requestJson = json.loads(requestJson)
    response = requests.post(site + url, json=requestJson)

    assert response.status_code == 200


def test_carParkEnterACar():
    url = "api/carpark/enter"
    Input = {
        "card_info": "cardInformation",
        "enterTime": "2022-12-02 17:00"
    }

    requestJson = json.dumps(Input, indent=4)
    requestJson = json.loads(requestJson)
    response = requests.post(site + url, json=requestJson)

    assert response.status_code == 200


def test_carParkCalculatePrice():
    url = "api/carpark/calculatePrice"
    Input = {
        "card_info": "cardInformation",
        "time": "2022-12-02 18:30"
    }

    requestJson = json.dumps(Input, indent=4)
    requestJson = json.loads(requestJson)
    response = requests.post(site + url, json=requestJson)

    assert response.status_code == 200


def test_carParkExitACar():
    url = "api/carpark/exit"
    Input = {
        "card_info": "cardInformation",
        "exitTime": "2022-12-02 19:00"
    }

    requestJson = json.dumps(Input, indent=4)
    requestJson = json.loads(requestJson)
    response = requests.post(site + url, json=requestJson)

    assert response.status_code == 200


def test_UserDelete():
    url = "api/user/delete"
    Input = {
        "card_info": "cardInformation"
    }

    requestJson = json.dumps(Input, indent=4)
    requestJson = json.loads(requestJson)
    response = requests.post(site + url, json=requestJson)

    assert response.status_code == 200
