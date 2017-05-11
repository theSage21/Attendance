import os
import tools
import bottle


# ------------------------------------------------------------
# ------------------------------------------------------------
# --------------HELPERS for WEB
# ------------------------------------------------------------
# ------------------------------------------------------------


def render(template, data=None):
    data = data if data is not None else dict()
    with tools.Config() as config:
        template_dir = config.C['directories']['templates']
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
    img = bottle.request.files.get('upload')
    name = ''.join(tools.letter() for _ in range(50))
    ext = img.filename.split('.')[-1]
    name = name + ext
    with tools.Config() as config:
        folder = config.C['directories']['photos']
        path = os.path.join(folder, name)
    img.save(path)
    return {'ident': name}


@app.post('/image/label')
def label_image():
    return {'status': 'Success'}


@app.post('/image/mark')
def mark_attendance():
    return {'present': []}


@app.post('/user')
def user():
    json = bottle.request.json
    token = json['token']
    status, details = tools.get_user_details(token)
    details.update({'status': status})
    return details


@app.post('/user/login')
def user_login():
    json = bottle.request.json
    user, password = json['user'], json['password']
    status, token = tools.login_user(user, password)
    return {'status': status, 'token': token}


@app.post('/user/logout')
def user_logout():
    json = bottle.request.json
    token = json['token']
    tools.logout_user(token)
    return {'status': True}


@app.post('/user/signup')
def user_signup():
    json = bottle.request.json
    user, password, kind = json['user'], json['password'], json['kind']
    status = tools.add_user(user, password, kind)
    return {'status': status}

# --------------------------------------------------------------
# --------------------------------------------------------------
# ------------------MAIN
# --------------------------------------------------------------
# --------------------------------------------------------------


@app.get('/static/<path:path>')
def static_server(path):
    with tools.Config() as config:
        root = config.C['directories']['static']
    return bottle.static_file(path, root=root)


if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8080, debug=True)
