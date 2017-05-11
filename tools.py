import random


def letter():
    return random.choice('asdfghjklqwertyuiopmnzxcvb1234567890')


def get_user_details(config, token):
    if token not in config['tokens']:
        kind, name, status = None, None, False
    else:
        name = config['tokens'][token]
        kind = config['users'][name]['kind']
        status = True
    return status, kind, name


def login_user(config, username, password):
    token, status = None, None
    if username in config['users']:
        pwd = config['users'][username]['pwd']
        status = (password == pwd)
    # ----------------
    if status:
        token = ''.join(letter() for _ in range(50))
        config['tokens'][token] = username
    return status, token, config


def logout_user(config, token):
    if token in config['tokens']:
        config['tokens'].pop(token)
    return config


def add_user(config, name, password, kind):
    if name not in config['users']:
        config['users'][name] = {'pwd': password,
                                 'kind': kind}
        status = True
    else:
        status = False
    return status, config
