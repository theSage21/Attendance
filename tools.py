import os
import json
import time
import random


class Config:
    "Use with `with`. In case of an exception, nothing is comitted"
    def __init__(self, path='config.json'):
        self.path = path

    def load(self):
        if not os.path.exists(self.path):
            with open(self.path, 'w') as fl:
                json.dump({}, fl)
        with open(self.path, 'r') as fl:
            self.C = json.loads(fl.read())

    def save(self):
        with open(self.path, 'w') as fl:
            json.dump(self.C, fl, indent=4)

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, type, value, trace):
        self.save()
        return True


def letter():
    return random.choice('asdfghjklqwertyuiopmnzxcvb1234567890')


def approve_user(token, user, lecture):
    status = False
    valid_request = False
    with Config() as config:
        if token in config.C['tokens'].keys():
            teacher = config.C['tokens'][token]
            if teacher in config.C['lectures'].keys():
                if lecture in config.C['lectures'][teacher].keys():
                    valid_request = True
        if valid_request:
            req_mems = config.C['lectures'][teacher][lecture]['__members__req']
            if user in req_mems:
                config.C['lectures'][teacher][lecture]['__members__req']\
                      .remove(user)
                config.C['lectures'][teacher][lecture]['__members__']\
                      .append(user)
                status = True
    return status


def get_pending_user_requests_to_join_class(token):
    status, pending = False, dict()
    with Config() as config:
        if token in config.C['tokens'].keys():
            teacher = config.C['tokens'][token]
            lectures = config.C['lectures'][teacher]
            pending = {k: {'req': v['__members__req'],
                           'mem': v['__members__']}
                       for k, v in lectures.items()}
            status = True
    return status, pending


def register_for_class_request(token, teach, lec):
    status = False
    message = 'An unknown error occured'
    with Config() as config:
        eligible = False
        if token in config.C['tokens'].keys():
            user = config.C['tokens'][token]
            if teach in config.C['users'].keys():
                if config.C['users'][teach]['kind'] == 'Teacher':
                    if lec in config.C['lectures'][teach].keys():
                        lecture = config.C['lectures'][teach][lec]
                        mem = lecture['__members__']
                        mem_req = lecture['__members__req']
                        if user in mem:
                            message = 'You are already in this class'
                        elif user in mem_req:
                            message = 'You have already requested'
                        else:
                            eligible = True
                    else:
                        message = 'This lecture does not exist'
                else:
                    message = 'This user is not a teacher'
            else:
                message = 'The user you mentioned as a Teacher does not exist'
        else:
            message = 'You are not logged in.'
        if eligible:
            config.C['lectures'][teach][lec]['__members__req'].append(user)
            status = True
            message = 'Successful request'
    return status, message


def remove_image(images_to_remove, token):
    status = False
    with Config() as config:
        if token in config.C['tokens'].keys():
            name = config.C['tokens'][token]
            for path in images_to_remove:
                config.C['users'][name]['images'].remove(path)
            status = True
    return status


def add_image(path, token):
    with Config() as config:
        if token in config.C['tokens'].keys():
            name = config.C['tokens'][token]
            config.C['users'][name]['images'].append(path)


def mark_attendance(path, token, lecture):
    with Config() as config:
        if token in config.C['tokens'].keys():
            name = config.C['tokens'][token]
            stamp = time.time()
            identified_people = []  # TODO: Identified people is the AI
            attendance = {'path': path, 'names': identified_people}
            if lecture not in config.C['lectures'][name].keys():
                lec = {stamp: attendance,
                       '__members__': [],
                       '__members__req': []}
                config.C['lectures'][name][lecture] = lec
            else:
                config.C['lectures'][name][lecture][stamp] = attendance


def get_user_details(token):
    with Config() as config:
        if token not in config.C['tokens'].keys():
            details, status = dict(), False
        else:
            name = config.C['tokens'][token]
            details = dict(config.C['users'][name])
            details['name'] = name
            details.pop('pwd')
            status = True
    return status, details


def login_user(username, password):
    with Config() as config:
        token, status = None, None
        if username in config.C['users'].keys():
            pwd = config.C['users'][username]['pwd']
            status = (password == pwd)
        # ----------------
        if status:
            while True:
                token = ''.join(letter() for _ in range(50))
                if token not in config.C['tokens'].keys():
                    break
            config.C['tokens'][token] = username
    return status, token


def logout_user(token):
    with Config() as config:
        if token in config.C['tokens'].keys():
            config.C['tokens'].pop(token)


def add_user(name, password, kind):
    with Config() as config:
        if name not in config.C['users'].keys():
            config.C['users'][name] = {'pwd': password,
                                       'kind': kind,
                                       'images': [],
                                       'labels': []}
            status = True
        else:
            status = False
    return status
