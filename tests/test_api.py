import os

os.environ["DATABASE_URL"] = "sqlite://"  # use in-memory db

import unittest  # noqa: E402
from datetime import datetime  # noqa: E402

from flask import current_app  # noqa: E402

from participants.app import db  # noqa: E402
from participants.app.models import Participant  # noqa: E402
from participants.registry import create_app  # noqa: E402


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.context = self.app.app_context()
        self.context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.client = None
        self.context.pop()
        self.app = None
        self.context = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_create(self):
        p = Participant.query.get("sgg")
        assert p is None
        data = {
            "firstname": "Stephen",
            "lastname": "Gaffney",
            "phone": "07777777777",
            "address1": "Street line 1",
            "address2": "Street line 2",
            "address3": "Street line 3",
            "town": "Springfield",
            "postcode": "94024",
            "country": "USA",
            "dob": "1900-01-01",
        }
        # p = Participant(ref_id='sgg')
        response = self.client.post("/participant/sgg", json=data)
        assert response.status_code == 200

        # Check output matches input
        out_data = response.json
        out_data.pop("uri")
        out_data.pop("ref_id")
        assert out_data == data

        p = Participant.query.get("sgg")
        assert p is not None

        # Test lookup
        response = self.client.get("/participant/sgg", json=data)
        with current_app.test_request_context():
            assert response.json == p.to_dict()
        out_data = response.json
        out_data.pop("uri")
        out_data.pop("ref_id")
        assert out_data == data

        assert p.firstname == "Stephen"
        assert p.dob == datetime.strptime("1900-01-01", "%Y-%m-%d").date()

        # Post for existing participant should fail
        response = self.client.post("/participant/sgg", json=data)
        assert response.status_code == 409

        # Modify participant sgg
        response = self.client.put(
            "/participant/sgg",
            json={
                "firstname": "Stefan",
                "dob": "1900-01-02",
            },
        )
        assert response.status_code == 200
        p = Participant.query.get("sgg")
        assert p.firstname == "Stefan"
        assert p.dob == datetime.strptime("1900-01-02", "%Y-%m-%d").date()

        # Check failure on unknown data field for post and modify
        bad_data = data.copy()
        bad_data.update({"bad_field": "bad_field_value"})
        response = self.client.put("/participant/sgg", json=bad_data)
        assert response.status_code == 400
        response = self.client.post("/participant/new1", json=bad_data)
        assert response.status_code == 400

        # Test deletion
        response = self.client.delete("/participant/sgg")
        assert response.status_code == 200
