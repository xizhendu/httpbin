#!/usr/bin/env python3

# Created by xizhendu at 10/5/21

"""
rfc:
- validation with specific roles

"""

import requests
import json
import sys
from common.config import service_config


# Define the running environment
# running_environment_file = 'environments/' + sys.argv[1] + '.yml'
running_environment_file = 'environments/running.yml'

# Read yaml file
# global running_config
running_config = service_config(running_environment_file)

auth_host = running_config['auth']['host']
auth_port = running_config['auth']['port']
auth_path = running_config['auth']['path']
if str(auth_port) == '443':
    jwt_validator_url = 'https://' + auth_host + auth_path + '/' + 'jwt/validator'
else:
    jwt_validator_url = 'http://' + auth_host + ':' + str(auth_port) + auth_path + '/jwt/validator'
iot_request_type = running_config['auth']['iot_request_types']['/jwt/validator']

print("""
jwt_validator_url: {0}
iot_request_type: {1}
""".format(jwt_validator_url, iot_request_type))


def validator(jwt_validator_url=None, jwt_authorization_value=None):
    print("""
    Processing with module common/jwt/validator...
    URL: {0}
    """.format(jwt_validator_url))
    _json = {
        "foo": "bar"
    }
    headers = {
        "Content-Type": "application/json",
        "X-Iot-Request-Type": iot_request_type,
        "Authorization": jwt_authorization_value
    }
    print("[Auth-Manager/JWT-Validator/Client] Sending request headers: \n", headers)
    response = requests.request("POST", url=jwt_validator_url, headers=headers, data=json.dumps(_json))
    _response_json = response.json()
    print(_response_json)
    print('Completing with common/jwt/validator...')
    return _response_json


