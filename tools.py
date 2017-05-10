import random

def login_user(config, username, password):
    users = config['users']
    if username not in users:
        status = None
    else:
        pwd = config['users'][username]
        status = password == pwd
    if status:
        token = ''.join(random.choice('asdfghjklqwertyuiopmnzxcvb1234567890')
                for _ in range(50))
        config['tokens'][token] = username
    return status, token, config

def logout_user(config, token):
    if token in config['tokens']:
        config['tokens'].pop(token)
    return config


def add_user(config, name, password):
    if name not in config['users']:
        config['users'][name] = password
        status = True
    else:
        status = False
    return status, config
