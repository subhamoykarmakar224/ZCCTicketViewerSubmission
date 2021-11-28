import os
from Constants import *


def if_path_exists(path):
    return os.path.exists(path)


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


def clear_user_data():
    if os.path.exists(URI_USER_DATA_FILE):
        os.remove(URI_USER_DATA_FILE)


def write_user_domain_name(domain):
    f = open(URI_DOMAIN_DATA_FILE, 'w')
    f.write(domain)
    f.close()


def write_domain_to_file():
    if read_user_domain_name() == '' or read_user_domain_name() != os.environ.get(ENV_KEY_DOMAIN):
        domain_val = os.environ.get(ENV_KEY_DOMAIN)
        write_user_domain_name(domain_val)


def read_user_domain_name():
    if not os.path.exists(URI_DOMAIN_DATA_FILE):
        return ''
    lns = ['']
    with open(URI_DOMAIN_DATA_FILE, 'r') as l:
        lns = l.readlines()

    if len(lns) > 0: lns = lns[0]
    else: lns = ''
    return lns


def write_user_data(name, role):
    f = open(URI_USER_DATA_FILE, 'w')
    f.write(name + '\n')
    f.write(role + '\n')
    f.close()


def get_user_data():
    if not if_path_exists(URI_USER_DATA_FILE):
        return []
    lines = []
    with open(URI_USER_DATA_FILE, 'r') as l:
        lines = l.readlines()

    return [lines[0], lines[1], read_user_domain_name()]


def get_url_data_from_file():
    uri_resource_file = URI_RESOURCE_FILE
    ln = []

    if not if_path_exists(uri_resource_file):
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


def write_url_data_to_file(prev, next, cur_page):
    uri_resource_file = URI_RESOURCE_FILE
    f = open(uri_resource_file, 'w')
    f.write("prev:" + str(prev) + "\n")
    f.write("next:" + str(next) + "\n")
    f.write("page:" + str(cur_page) + "\n")
    f.close()


