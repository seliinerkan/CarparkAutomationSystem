import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import math



db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    card_info = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    user_name = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(64), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_cardInfo(cls, cardInfo):
        return cls.query.filter_by(card_info=cardInfo).first()


class carPark_information(db.Model):
    card_info = db.Column(db.String(64), nullable=False, primary_key=True)
    enter_time = db.Column(db.DateTime())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_cardInfo(cls, cardInfo):
        return cls.query.filter_by(card_info=cardInfo).first()

class carPark_prices(db.Model):
    totalMinutes = db.Column(db.Integer(), primary_key=True)
    price = db.Column(db.Integer())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_minutes(cls, minutes):
        return cls.query.filter_by(totalMinutes=minutes).first()


    def findLower(self, priceList):
        lowerPrice = priceList[0]
        for price in priceList:
            if lowerPrice.totalMinutes > price.totalMinutes:
                lowerPrice = price


    @classmethod
    def calculatePrice(cls, minutes):
        price = cls.query.filter(cls.totalMinutes >= minutes).order_by(sqlalchemy.asc(cls.totalMinutes)).first()
        if not price:
            maxPrice = cls.query.filter(cls.totalMinutes < minutes).order_by(sqlalchemy.desc(cls.totalMinutes)).first()
            maxPrice = maxPrice.price
            return math.ceil(minutes / 1440) * maxPrice

        return price.price







