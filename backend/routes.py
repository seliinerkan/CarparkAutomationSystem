from flask import request
from flask_restx import Api, Resource, fields
from datetime import datetime

from .models import Users, carPark_information, carPark_prices

rest_api = Api(version="1.0", title="Users API")

"""
    User Operators
"""
@rest_api.route('/api/users/register')
class Register(Resource):
    def post(self):
        req_data = request.get_json()

        cardInfo = req_data.get("card_info")
        email = req_data.get("email")
        phoneNum = req_data.get("phone_num")
        username = req_data.get("username")
        if not(cardInfo and email and phoneNum and username):
            return {"success": False,
                    "msg": "Missing Data"}, 400


        userExist = Users.get_by_cardInfo(cardInfo)
        if userExist:
            return {"success": False,
                    "msg": "The card info already taken."}, 400

        newUser = Users()
        newUser.card_info = cardInfo
        newUser.email = email
        newUser.phone_number = phoneNum
        newUser.user_name = username
        newUser.save()

        return {"success": True,
                "userID": newUser.id,
                "msg": "The user was successfully registered."}, 200

@rest_api.route('/api/user')
class get_user_values(Resource):
    def post(self):
        req_data = request.get_json()
        cardInfo = req_data.get("card_info")

        userExist = Users.get_by_cardInfo(cardInfo)
        if not userExist:
            return {"success": False,
                    "msg": "The card info not found."}, 400

        return {"success": True,
                "user": {
                    "userID": userExist.id,
                    "username": userExist.user_name,
                    "phone_num": userExist.phone_number,
                    "email": userExist.email
                },
                "msg": "User information found."}, 200

@rest_api.route('/api/user/update')
class user_updates(Resource):
    def post(self):
        req_data = request.get_json()
        cardInfo = req_data.get("card_info")

        userExist = Users.get_by_cardInfo(cardInfo)
        if not userExist:
            return {"success": False,
                    "msg": "The card info not found."}, 400

        email = req_data.get("email")
        if email:
            userExist.email = email

        phoneNum = req_data.get("phone_num")
        if phoneNum:
            userExist.phone_number = phoneNum

        username = req_data.get("username")
        if username:
            userExist.user_name = username

        userExist.save()
        return {"success": True,
                "msg": "The user was successfully updated."}, 200

"""
    Car Park Operators
"""

@rest_api.route('/api/carpark/enter')
class enterCar(Resource):
    def post(self):
        req_data = request.get_json()
        cardInfo = req_data.get("card_info")
        enterTime = req_data.get("enterTime")

        time = datetime.strptime(enterTime, "%Y-%m-%d %H:%M")

        carExist = carPark_information.get_by_cardInfo(cardInfo)
        if carExist:
            return {"success": False,
                    "msg": "The car is in the park."}, 400

        carParkInfo = carPark_information()
        carParkInfo.card_info = cardInfo
        carParkInfo.enter_time = time
        carParkInfo.save()

        return {"success": True,
                "msg": "The car was successfully entered."}, 200

@rest_api.route('/api/carpark/calculatePrice')
class calculatePrice(Resource):
    def post(self):
        req_data = request.get_json()
        cardInfo = req_data.get("card_info")
        time = req_data.get("time")

        try:
            time = datetime.strptime(time, "%Y-%m-%d %H:%M")
        except:
            return {"success": False,
                    "msg": "The time information does not match the format."}, 400

        carExist = carPark_information.get_by_cardInfo(cardInfo)
        if not carExist:
            return {"success": False,
                    "msg": "The car is not in the park."}, 400

        totalTime = time - carExist.enter_time
        totalMin = totalTime.total_seconds() // 60

        if totalMin <= 0:
            return {"success": False,
                    "msg": "An error occured"}, 400

        totalPrice = carPark_prices.calculatePrice(totalMin)

        return {"success": True,
                "totalTime": totalMin,
                "totalPrice": totalPrice,
                "msg": "The calculation done successfully."}, 200



@rest_api.route('/api/carpark/exit')
class exitCar(Resource):
    def post(self):
        req_data = request.get_json()
        cardInfo = req_data.get("card_info")
        exitTime = req_data.get("exitTime")

        try:
            time = datetime.strptime(exitTime, "%Y-%m-%d %H:%M")
        except:
            return {"success": False,
                    "msg": "The time information does not match the format."}, 400

        carExist = carPark_information.get_by_cardInfo(cardInfo)
        if not carExist:
            return {"success": False,
                    "msg": "The car is not in the park."}, 400

        totalTime = time - carExist.enter_time
        totalMin = totalTime.total_seconds() // 60

        carExist.delete()

        if totalMin <= 0:
            return {"success": False,
                    "msg": "An error occured"}, 400

        totalPrice = carPark_prices.calculatePrice(totalMin)

        return {"success": True,
                "totalTime": totalMin,
                "totalPrice": totalPrice,
                "msg": "The car was successfully exit."}, 200


"""
    Price Operators
"""
@rest_api.route('/api/prices/add')
class add_price(Resource):
    def post(self):
        req_data = request.get_json()

        minutes = req_data.get("minutes")
        price = req_data.get("price")

        priceExist = carPark_prices.get_by_minutes(minutes)
        if priceExist:
            return {"success": False,
                    "msg": "The price info already taken."}, 400

        carPark_price = carPark_prices()
        carPark_price.totalMinutes = minutes
        carPark_price.price = price

        carPark_price.save()
        return {"success": True,
                "msg": "The car park price value successfully added."}, 200

@rest_api.route('/api/prices/update')
class update_price(Resource):
    def post(self):
        req_data = request.get_json()

        minutes = req_data.get("minutes")
        price = req_data.get("price")

        priceExist = carPark_prices.get_by_minutes(minutes)
        if not priceExist:
            return {"success": False,
                    "msg": "The price info not found."}, 400

        price = req_data.get("price")
        if price:
            priceExist.price = price

        priceExist.save()
        return {"success": True,
                "msg": "The car park price value successfully updated."}, 200

@rest_api.route('/api/prices/delete')
class update_price(Resource):
    def post(self):
        req_data = request.get_json()
        minutes = req_data.get("minutes")

        priceExist = carPark_prices.get_by_minutes(minutes)
        if not priceExist:
            return {"success": False,
                    "msg": "The price info not found."}, 400

        priceExist.delete()
        return {"success": True,
                "msg": "The car park price value successfully deleted."}, 200


