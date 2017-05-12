import json
import random


class Config:
    "Use with `with`. In case of an exception, nothing is comitted"
    def __init__(self, path='config.json'):
        self.path = path

    def load(self):
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


def add_image(path, token):
    with Config() as config:
        if token in config.C['tokens'].keys():
            name = config.C['tokens'][token]
            config.C['users'][name]['images'].append(path)


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
            print('User token found. Logging out token {}'.format(token))
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
