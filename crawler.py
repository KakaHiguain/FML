# -*- coding:Windows-1252 -*-
import logging
import requests


# TODO: refactor this file
def get_page(url, headers=None):
    sessions = requests.session()
    while True:
        try:
            response = sessions.post(url, headers=headers)
            break
        except:
            logging.error('Retry!')
    return response.text


def get_page_json(url, headers):
    sessions = requests.session()
    while True:
        try:
            response = sessions.post(url, headers=headers)
            break
        except:
            logging.error('Retry!')
    return response.json()
