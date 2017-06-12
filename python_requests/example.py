"""
Usage

python example.py <hotel_id> <partner_id> <api_key>
"""
import argparse
import base64

import requests

CONNECT_API_AUTH_ENDPOINT = 'https://analytics.trustyou.com/connect/api/v1.0/auth'
CONNECT_API_HOTEL_ENDPOINT = 'https://analytics.trustyou.com/connect/api/v1.0/hotels'


def get_auth_token(partner_name, api_key):
    """Returns the API authorization token. Use this for subsequent calls.
 
    When the token expires, you can get another one using logic similar to what this function
    illustrates

    :param str partner_name: the partner's name for use in the API
    :param str api_key: the partner's API key, for use in the API

    :rtype: str
    :return: A JWT token
    """
    authorization_raw_key = '{}:{}'.format(partner_name, api_key)

    # The ASCII decoding/encoding is specific to python, but might be required in other languages
    base64_encoded_key = base64.b64encode(authorization_raw_key.encode('ascii')).decode('ascii')

    auth_response = requests.post(
        CONNECT_API_AUTH_ENDPOINT,
        headers={
            'Authorization': 'Basic {}'
            .format(base64_encoded_key),
            'Content-type': 'application/json',
            'Accept': 'application/json'})

    token = auth_response.json()['access_token']  # response status code should be 201
    return token
 
def get_hotel_by_id(hotel_id, partner_name, api_key):
    """Using the token provided, call the endpoint.
 
    The token validity period is limited. If it expires, you should get another one

    :param str|None hotel_id: a hotel id to get the details for. If None, will retrieve many hotels
    :param str partner_name: see func::`get_auth_token`
    :param str api_key: see func::`get_auth_token`

    :rtype: requests.Response
    :return: a response object
    """
    token = get_auth_token(partner_name, api_key)

    url = CONNECT_API_HOTEL_ENDPOINT

    if hotel_id:
        url += '/{}'.format(hotel_id)

    get_hotels_resp = requests.get(url, headers={'Authorization': 'Bearer {}'.format(token)})

    return get_hotels_resp


def get_parser():
    """Return a configured ArgumentParser"""
    parser = argparse.ArgumentParser()

    parser.add_argument('partner_name', help="Your partner name for usage in the API", type=str)
    parser.add_argument('api_key', help="The API key to use for accessing the API", type=str)
    parser.add_argument(
        'hotel_id',
        help="[OPTIONAL] A hotel ID for which to request data. If not provided, will retrieve many "
             "hotels", type=str, default=None, nargs='?')

    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()

    get_hotel_response = get_hotel_by_id(args.hotel_id, args.partner_name, args.api_key)

    # You can pipe this to a file.
    print(get_hotel_response.text)
