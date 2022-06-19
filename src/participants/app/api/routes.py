"""Routes for participant endpoint."""

from flask import abort, request

from .. import db
from ..models import Participant
from . import api


@api.route("/participant/<string:ref_id>", methods=["GET"])
def lookup(ref_id):
    """Get participant metadata from reference number."""
    person = Participant.query.filter_by(ref_id=ref_id).first_or_404()
    return person.to_dict()


@api.route("/participant/<string:ref_id>", methods=["POST"])
def add(ref_id):
    """Add participant metadata using reference number."""
    if Participant.query.get(ref_id):
        abort(409)  # don't overwrite participant
    person = Participant(ref_id=ref_id)
    _update_and_commit_participant_from_request(person)
    return person.to_dict()


@api.route("/participant/<string:ref_id>", methods=["PUT"])
def modify(ref_id):
    """Modify participant metadata using reference number."""
    person = Participant.query.get_or_404(ref_id)  # record must exist
    _update_and_commit_participant_from_request(person)
    return person.to_dict()


@api.route("/participant/<string:ref_id>", methods=["DELETE"])
def remove(ref_id):
    """Modify participant metadata using reference number."""
    person = Participant.query.get_or_404(ref_id)  # record must exist
    db.session.delete(person)
    db.session.commit()
    return {
        "status": 200,
        "message": f"participant {ref_id} removed",
    }, 200


def _update_and_commit_participant_from_request(person: Participant) -> None:
    user_keys = set(request.json.keys())
    if user_keys.difference(person.mutable_fields):
        abort(404)
    person.update_from_dict(request.json)
    db.session.add(person)
    db.session.commit()
