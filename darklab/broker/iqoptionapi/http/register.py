"""Module for IQ option register resource."""

from darklab.broker.iqoptionapi.http.resource import Resource


class Register(Resource):
    """Class for IQ option register resource."""
    # pylint: disable=too-few-public-methods

    url = "register"
