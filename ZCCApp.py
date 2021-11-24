from urllib.parse import urlencode
import json
import requests
from bottle import route, template, redirect, static_file, error, request, response, run


@route('/')
def show_home():
    return template('index')


@error(404)
def error404(error):
    return template('error', error_msg='404 error. Nothing to see here')


run(host='localhost', port=3001, debug=True)
