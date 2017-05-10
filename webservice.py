import os
import json
import bottle

# READ CONFIG
with open('config.json', 'r') as fl:
    CFG = json.loads(fl.read())

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
    return {'status': True, 'token': 'asdf'}


@app.post('/user/logout')
def user_logout():
    return {'status': True}
