import os
import json
import tools
import bottle

# READ CONFIG
def load_cfg():
    with open('config.json', 'r') as fl:
        CFG = json.loads(fl.read())
    return CFG

def save_cfg(cfg):
    with open('config.json', 'w') as fl:
        json.dump(cfg, fl, indent=4)

CFG = load_cfg()
save_cfg(CFG)

# ------------------------------------------------------------
# ------------------------------------------------------------
# --------------HELPERS for WEB
# ------------------------------------------------------------
# ------------------------------------------------------------


def render(template, data=None):
    global CFG
    template_dir = CFG['directories']['templates']
    data = data if data is not None else dict()
    with open(os.path.join(template_dir, template)) as fl:
        html = fl.read()
    return bottle.template(html, **data)


# --------------------------------------------------------------
# --------------------------------------------------------------
# ------------------ROUTES
# --------------------------------------------------------------
# --------------------------------------------------------------
app = bottle.Bottle()


@app.get('/')
def home():
    return render('home.html')


@app.post('/image/upload')
def upload_image():
    return {'ident': None}


@app.post('/image/label')
def label_image():
    return {'status': 'Success'}


@app.post('/image/mark')
def mark_attendance():
    return {'present': []}


@app.get('/user')
def user():
    return {}


@app.post('/user/login')
def user_auth():
    global CFG
    json = bottle.request.json
    user, pasword = json['user'], json['password']
    status, token, CFG = tools.login_user(CFG, user, password)
    save_cfg(CFG)
    return {'status': status, 'token': token}


@app.post('/user/logout')
def user_logout():
    global CFG
    json = bottle.request.json
    token = json['token']
    status = tools.logout_user(CFG, token)
    save_cfg(CFG)
    return {'status': status}


@app.post('/user/add')
def user_signup():
    global CFG
    json = bottle.request.json
    user, pasword = json['user'], json['password']
    status, CFG = tools.add_user(CFG, user, password)
    save_cfg(CFG)
    return {'status': status}

# --------------------------------------------------------------
# --------------------------------------------------------------
# ------------------MAIN
# --------------------------------------------------------------
# --------------------------------------------------------------
@app.get('/static/<path:path>')
def static_server(path):
    return bottle.static_file(path, root=CFG['directories']['static'])

if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8080, debug=True)
