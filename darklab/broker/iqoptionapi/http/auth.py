"""Module for IQ Option http auth resource."""

from darklab.broker.iqoptionapi.http.resource import Resource


class Auth(Resource):
    """Class for IQ Option http auth resource."""
    # pylint: disable=too-few-public-methods

    url = "auth"
