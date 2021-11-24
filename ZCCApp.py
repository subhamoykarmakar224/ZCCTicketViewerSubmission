import math
from urllib.parse import urlencode
import json
import os
from datetime import datetime
import requests
from bottle import route, template, redirect, static_file, error, request, response, run


@route('/')
def base():
    uri_resource_file = './tmp/resource.txt'
    if os.path.exists(uri_resource_file):
        os.remove(uri_resource_file)
    redirect('/p1')


@route('/<pg:re:p*[0-9]*>')
def show_home(pg='#'):
    request_pg_num = 0
    if pg != "#":
        request_pg_num = int(pg[1:])
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
    if request.get_cookie('owat'):
        no_of_items = 25
        params['ticket_count'] = get_tickets_count()
        params['page_count'] = math.ceil(params['ticket_count'] / no_of_items)
        user_data = get_user_data()
        if user_data == []:
            get_user_information()
            user_data = get_user_data()
        params['name'] = user_data[0]
        params['role'] = user_data[1]
        # Get user data
        access_token = request.get_cookie('owat')
        bearer_token = 'Bearer ' + access_token
        header = {'Authorization': bearer_token}
        url = ""
        prev_pg_url, next_pg_url, cur_page = get_url_data_from_file()
        if next_pg_url == '' or prev_pg_url == '' or request_pg_num <= 0:
            url = 'https://zccsubhamoy.zendesk.com/api/v2/tickets.json?page[size]=25'
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
            return template('index', error_msg=error_msg)
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
            'client_id': 'zcc_oauth_app',
            'client_secret': '52391629c5df64127d24af9e1d2b18c4b70c257e5fccc0010bf336491861b03d',
            'redirect_uri': 'http://localhost:3001/handle_user_decision',
            'scope': 'read'
        }
        payload = json.dumps(parameters)
        header = {'Content-Type': 'application/json'}
        url = 'https://zccsubhamoy.zendesk.com/oauth/tokens'
        r = requests.post(url, data=payload, headers=header)
        if r.status_code != 200:
            error_msg = 'Failed to get access token with error {}'.format(r.status_code)
            return template('error', error_msg=error_msg)
        else:
            data = r.json()
            response.set_cookie('owat', data['access_token'])
            redirect('/')


def get_tickets_count():
    access_token = request.get_cookie('owat')
    bearer_token = 'Bearer ' + access_token
    header = {'Authorization': bearer_token}
    url = 'https://zccsubhamoy.zendesk.com/api/v2/tickets/count.json'
    r = requests.get(url, headers=header)
    data = r.json()
    return data['count']['value']


def get_user_information():
    if request.get_cookie('owat'):
        # Get user data
        access_token = request.get_cookie('owat')
        bearer_token = 'Bearer ' + access_token
        header = {'Authorization': bearer_token}
        url = 'https://zccsubhamoy.zendesk.com/api/v2/users/me.json'
        r = requests.get(url, headers=header)
        if r.status_code != 200:
            error_msg = 'Failed to get data with error {}'.format(r.status_code)
            return template('error', error_msg=error_msg)
        else:
            data = r.json()
            write_user_data(data['user']['name'], data['user']['role'])
    else:
        redirect_to_authentication()


def write_url_data_to_file(prev, next, cur_page):
    uri_resource_file = './tmp/resource.txt'
    f = open(uri_resource_file, 'w')
    f.write("prev:" + str(prev) + "\n")
    f.write("next:" + str(next) + "\n")
    f.write("page:" + str(cur_page) + "\n")
    f.close()


def get_url_data_from_file():
    uri_resource_file = './tmp/resource.txt'
    ln = []

    if not os.path.exists(uri_resource_file):
        return '', '', 0

    with open(uri_resource_file, 'r') as l:
        ln = l.readlines()
    if len(ln) == 0:
        return '', '', 0
    prev_url = ln[0][ln[0].index(':') + 1:]
    next_url = ln[1][ln[1].index(':') + 1:]
    cur_page_no = ln[2][ln[2].index(':') + 1:]

    if os.path.exists(uri_resource_file):
        os.remove(uri_resource_file)

    return prev_url.strip('\n'), next_url.strip('\n'), int(cur_page_no.strip('\n'))


def get_user_data():
    data_file = './tmp/user_data.txt'
    if not os.path.exists(data_file):
        return []
    lines = []
    with open(data_file, 'r') as l:
        lines = l.readlines()
    return [lines[0], lines[1]]


def write_user_data(name, role):
    data_file = './tmp/user_data.txt'
    f = open(data_file, 'w')
    f.write(name + '\n')
    f.write(role + '\n')
    f.close()


def clear_user_data():
    data_file = './tmp/user_data.txt'
    if os.path.exists(data_file):
        os.remove(data_file)


def data_cleaning_ticket(raw_data):
    data = []
    for t in raw_data['tickets']:
        data.append(
            {
                "id": t["id"],
                "created_at": t["created_at"],
                "status": t["status"],
                "priority": t["priority"],
                "subject": t["subject"]
            }
        )

    return data


def redirect_to_authentication():
    clear_user_data()
    parameters = {
        'response_type': 'code',
        'redirect_uri': 'http://localhost:3001/handle_user_decision',
        'client_id': 'zcc_oauth_app',
        'scope': 'read write'}
    url = 'https://zccsubhamoy.zendesk.com/oauth/authorizations/new?' + urlencode(parameters)
    redirect(url)


@error(404)
def error404(error):
    return template('error', error_msg='404 error. Page you are looking for does not exits.')


@error(500)
def error404(error):
    return template('error', error_msg='500 error. Internal Server Error. Please try again later.')


if __name__ == '__main__':
    uri_resource_file = './tmp/resource.txt'
    if os.path.exists(uri_resource_file):
        os.remove(uri_resource_file)
    run(host='localhost', port=3001, debug=True)
