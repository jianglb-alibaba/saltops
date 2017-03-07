#!  /usr/bin/python
# coding=utf-8

from saltjob.salt_https_api import salt_api_token
from saltops.settings import SALT_REST_URL, SALT_USER, SALT_PASSWORD


def token_id():
    s = salt_api_token(
        {
            "username": SALT_USER,
            "password": SALT_PASSWORD,
            "eauth": "pam"
        },
        SALT_REST_URL + "login",
        {}
    )
    test = s.run()
    salt_token = [i["token"] for i in test["return"]]
    salt_token = salt_token[0]
    return salt_token
