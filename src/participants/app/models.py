from collections import OrderedDict
from datetime import datetime

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

    @property
    def mutable_fields(self) -> set:
        return {
            "firstname",
            "lastname",
            "dob",
            "phone",
            "address1",
            "address2",
            "address3",
            "town",
            "postcode",
            "country",
        }

    def to_dict(self) -> OrderedDict:
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

    def update_from_dict(self, data: dict) -> None:
        for key in data:
            if key in self.mutable_fields:
                if key == "dob":
                    val = datetime.strptime(data[key], "%Y-%m-%d").date()
                else:
                    val = data[key]
                setattr(self, key, val)

    def get_uri(self):
        return url_for("api.lookup", ref_id=self.ref_id, _external=True)
