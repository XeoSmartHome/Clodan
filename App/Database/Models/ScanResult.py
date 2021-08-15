from ..connection import db
from mongoengine import StringField, BooleanField, DictField, DateTimeField


class ScanResult(db.Document):
    hostname = StringField()
    ip_address = StringField()
    encrypted_connection = BooleanField()
    protocol = StringField()
    certificate = DictField()
    timestamp = DateTimeField()
    country = StringField()
    country_code = StringField()

    def to_dict(self):
        return {
            'hostName': self.hostname,
            'ipAddress': self.ip_address,
            'isSecure': self.encrypted_connection,
            'protocol': self.protocol,
            'certificate': self.certificate,
            'timestamp': self.timestamp
        }