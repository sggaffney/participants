from ..models import Participant
from . import api


@api.route("/participant/<string:ref_id>", methods=["GET"])
def lookup(ref_id):
    person = Participant.query.filter_by(ref_id=ref_id).first_or_404()
    return person.to_dict()
