from flask import Blueprint

api = Blueprint("api", __name__)


@api.errorhandler(400)
def bad_request_error(e):
    return {
        "status": 400,
        "error": "bad request",
        "message": "invalid request",
    }, 400


@api.errorhandler(404)
def not_found_error(e):
    return {
        "status": 400,
        "error": "bad request",
        "message": "item not found",
    }, 400


@api.errorhandler(405)
def method_not_allowed_error(e):
    return {
        "status": 405,
        "error": "method not allowed",
    }, 405


# late import, to avoid circular dependencies
from . import routes  # noqa: E402, F401
