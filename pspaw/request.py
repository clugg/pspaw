"""
Python StrawPoll API Wrapper.

Provide one-liner functions for reqing JSON files and handling any
errors provided by the StrawPoll API.
"""

import json
import requests

from pspaw import __author__, __version__
from pspaw.errors import PSPAWBaseException

USERAGENT = "PSPAW v{} by {}".format(__version__, __author__)

def _handle(req):
    """
    Parse JSON from a request string and handle any errors
    thrown by StrawPoll's API.

    Args:
        req (str): A JSON string returned from StrawPoll's API.

    Returns:
        dict: Result from parsing the inputted JSON string.

    Raises:
        PSPAWBaseException: when StrawPoll's API returns an error.
    """

    req = req.strip()
    if req == "Bad Request":
        raise PSPAWBaseException(req)
    else:
        req = json.loads(req)

    if "error" in req:
        raise PSPAWBaseException(req["code"], req["error"])

    return req

def post(url, params={}):
    """
    Performs a POST request to the specified URL
    with the specified paramaters.

    Args:
        url (str): URL to perform POST request to.
        params (Optional[dict]): Paramaters for the POST request. Defaults to {}.

    Returns:
        dict: Result from parsing the JSON returned by the POST request.
    """

    return _handle(requests.post(url, json=params, headers={"User-Agent": USERAGENT, "Content-Type": "application/json"}).text)

def get(url, params={}):
    """
    Performs a GET request to the specified URL
    with the specified paramaters.

    Args:
        url (str): URL to perform GET request to.
        params (Optional[dict]): Paramaters for the GET request. Defaults to {}.

    Returns:
        dict: Result from parsing the JSON returned by the GET request.
    """

    return _handle(requests.get(url, params=params, headers={"User-Agent": USERAGENT}).text)
