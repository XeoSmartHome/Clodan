from ..connection import db
from mongoengine.fields import IntField, StringField


class IpRange(db.Document):
    first_ip = IntField()
    last_ip = IntField()
    country_code = StringField()
    country = StringField()

    # def __init__(self, first_ip: int, last_ip: int, country_code: str, country: str):
    #    super(IpRange, self).__init__(first_ip=first_ip, last_ip=last_ip, country_code=country_code, country=country)
