# -*- coding:Windows-1252 -*-
import logging
import requests


def get_page(url, headers):
    sessions = requests.session()
    while True:
        try:
            response = sessions.post(url, headers=headers)
            break
        except:
            logging.error('Retry!')
    return response.text
