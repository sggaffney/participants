from collections import OrderedDict

from flask import url_for

from . import db


class Participant(db.Model):
    __tablename__ = "participants"
    ref_id = db.Column(db.String(255), primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    dob = db.Column(db.Date())
    phone = db.Column(db.String(255))  # start with single phone number
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    address3 = db.Column(db.String(255))
    town = db.Column(db.String(255))
    postcode = db.Column(db.String(255))
    country = db.Column(db.String(255))

    def to_dict(self):
        return OrderedDict(
            [
                ("uri", self.get_uri()),
                ("ref_id", self.ref_id),
                ("firstname", self.firstname),
                ("lastname", self.lastname),
                ("dob", self.dob.strftime("%Y-%m-%d") if self.dob else None),
                ("phone", self.phone),
                ("address1", self.address1),
                ("address2", self.address2),
                ("address3", self.address3),
                ("town", self.town),
                ("postcode", self.postcode),
                ("country", self.country),
            ]
        )

    def get_uri(self):
        return url_for("api.lookup", ref_id=self.ref_id, _external=True)
