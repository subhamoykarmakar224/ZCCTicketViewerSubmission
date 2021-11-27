import math
from urllib.parse import urlencode
import json
import requests
from bottle import route, template, redirect, error, request, response, run
from Helper import *
from dotenv import load_dotenv
import os
from os.path import join, dirname


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@route('/')
def base():
    if if_path_exists(URI_RESOURCE_FILE):
        os.remove(URI_RESOURCE_FILE)
    write_domain_to_file()
    redirect('/1')


@route('/<pg>')
def show_home(pg='#'):
    write_domain_to_file()
    request_pg_num = 0
    if pg != "#":
        request_pg_num = int(pg)
    params = {
        'name': '',
        'role': '',
        'error': '',
        'pg_start': '',
        'pg_end': '',
        'pg_total': '',
        'btn-previous-disable': '',
        'btn-next-disable': '',
    }

    if request.get_cookie(KEY_COOKIE_NAME):
        params['ticket_count'] = get_tickets_count()
        params['page_count'] = math.ceil(params['ticket_count'] / APP_PER_PAGE_ITEM_COUNT)
        user_data = get_user_data()
        if user_data == []:
            get_user_information()
            user_data = get_user_data()
        params['name'] = user_data[0]
        params['role'] = user_data[1]
        params['domain'] = user_data[2]

        # Get user data
        access_token = request.get_cookie(KEY_COOKIE_NAME)
        bearer_token = 'Bearer ' + access_token
        header = {'Authorization': bearer_token}
        url = ""
        prev_pg_url, next_pg_url, cur_page = get_url_data_from_file()
        if abs(cur_page - request_pg_num) > 1:
            write_url_data_to_file(prev_pg_url, next_pg_url, cur_page)
            return template('error', error_msg='404 error. Page you are looking for does not exits.')

        if next_pg_url == '' or prev_pg_url == '' or request_pg_num <= 0:
            url = 'https://' + read_user_domain_name() + '.zendesk.com/api/v2/tickets.json?page[size]=' + str(APP_PER_PAGE_ITEM_COUNT)
            params['cur_page'] = 1
            params['btn-previous-disable'] = 'disabled'
        elif request_pg_num > cur_page:
            url = next_pg_url
            params['cur_page'] = request_pg_num
        elif request_pg_num < cur_page:
            url = prev_pg_url
            params['cur_page'] = request_pg_num

        if request_pg_num == params['page_count']:
            params['btn-next-disable'] = 'true'
        else:
            params['btn-next-disable'] = 'false'

        r = requests.get(url, headers=header)
        if r.status_code != 200:
            error_msg = 'Failed to get data with error {}'.format(r.status_code)
            return template('error', error_msg=error_msg)
        else:
            raw_data = r.json()
            if params['cur_page'] >= params['page_count']:
                params['cur_page'] = params['page_count']
                next_pg_url = url
            else:
                next_pg_url = raw_data['links']['next']
            prev_pg_url = raw_data['links']['prev']
            write_url_data_to_file(prev_pg_url, next_pg_url, params['cur_page'])
            params['tickets'] = data_cleaning_ticket(raw_data)
    else:
        redirect_to_authentication()

    return template('index', params)


@route('/handle_user_decision')
def handle_decision():
    if 'error' in request.query_string:
        return template('error', error_msg=request.query.error_description)
    else:
        # Get access token
        parameters = {
            'grant_type': 'authorization_code',
            'code': request.query.code,
            'client_id': get_env_value(ENV_KEY_CLIENT_ID),
            'client_secret': get_env_value(ENV_KEY_CLIENT_SECRET),
            'redirect_uri': 'http://localhost:3001/handle_user_decision',
            'scope': 'read'
        }
        payload = json.dumps(parameters)
        header = {'Content-Type': 'application/json'}
        url = 'https://' + read_user_domain_name() + '.zendesk.com/oauth/tokens'
        r = requests.post(url, data=payload, headers=header)
        if r.status_code != 200:
            error_msg = 'Failed to get access token with error {}'.format(r.status_code)
            return template('error', error_msg=error_msg)
        else:
            data = r.json()
            response.set_cookie(KEY_COOKIE_NAME, data['access_token'])
            redirect('/')


def get_tickets_count():
    access_token = request.get_cookie(KEY_COOKIE_NAME)
    bearer_token = 'Bearer ' + access_token
    header = {'Authorization': bearer_token}
    url = 'https://' + read_user_domain_name() + '.zendesk.com/api/v2/tickets/count.json'
    r = requests.get(url, headers=header)
    data = r.json()
    return data['count']['value']


def get_user_information():
    if request.get_cookie(KEY_COOKIE_NAME):
        # Get user data
        access_token = request.get_cookie(KEY_COOKIE_NAME)
        bearer_token = 'Bearer ' + access_token
        header = {'Authorization': bearer_token}
        url = 'https://' + read_user_domain_name() + '.zendesk.com/api/v2/users/me.json'
        r = requests.get(url, headers=header)
        if r.status_code != 200:
            error_msg = 'Failed to get data with error {}'.format(r.status_code)
            return template('error', error_msg=error_msg)
        else:
            data = r.json()
            write_user_data(data['user']['name'], data['user']['role'])
    else:
        redirect_to_authentication()


def redirect_to_authentication():
    clear_user_data()
    parameters = {
        'response_type': 'code',
        'redirect_uri': 'http://localhost:3001/handle_user_decision',
        'client_id': get_env_value(ENV_KEY_CLIENT_ID),
        'scope': 'read write'
    }
    url = 'https://' + read_user_domain_name() + '.zendesk.com/oauth/authorizations/new?' + urlencode(parameters)
    redirect(url)


def get_env_value(key):
    return os.environ.get(key, '')



@error(404)
def error404(error):
    return template('error', error_msg='404 error. Page you are looking for does not exits.')


@error(500)
def error404(error):
    return template('error', error_msg='500 error. Internal Server Error. Please try again later.')


if __name__ == '__main__':
    if os.path.exists(URI_RESOURCE_FILE):
        os.remove(URI_RESOURCE_FILE)
    run(host=APP_HOST, port=APP_PORT, debug=True)
    # print(os.environ.get(ENV_KEY_DOMAIN_1), os.environ.get(ENV_KEY_USERNAME_1))
