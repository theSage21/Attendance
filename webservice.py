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
    # This is the main thing. Actually this is the only page on
    # This entire site. Everything else is an API.
    return render('home.html')


@app.post('/image/upload')
def upload_image():
    # I could not figure out how JSON file uploads worked.
    # I'm sticking to form uploads for now.
    token = bottle.request.forms.get('usertoken')
    if tools.get_user_details(token)[0]:
        img = bottle.request.files.get('upload')
        ext = img.filename.split('.')[-1]
        with tools.Config() as config:
            folder = config.C['directories']['photos']
        while True:
            name = ''.join(tools.letter() for _ in range(50))
            name = '{}.{}'.format(name, ext)
            if name not in os.listdir(folder):
                break
        path = os.path.join(folder, name)
        img.save(path)
        tools.add_image(path, token)
    return bottle.redirect('/')


@app.post('/image/delete')
def delete_images():
    json = bottle.request.json
    images_to_remove = json['images_to_remove']
    token = json['token']
    status = tools.remove_image(images_to_remove, token)
    return {'status': status}


@app.post('/image/mark')
def mark_attendance():
    # Mark an image with attendance.
    token = bottle.request.forms.get('usertoken')
    lecture = bottle.request.forms.get('lecture')
    if tools.get_user_details(token)[0]:
        img = bottle.request.files.get('upload')
        ext = img.filename.split('.')[-1]
        with tools.Config() as config:
            folder = config.C['directories']['photos']
        while True:
            name = ''.join(tools.letter() for _ in range(50))
            name = '{}.{}'.format(name, ext)
            if name not in os.listdir(folder):
                break
        path = os.path.join(folder, name)
        img.save(path)
        tools.mark_attendance(path, token, lecture)
    return bottle.redirect('/')


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


@app.post('/user/request/class')
def user_register_for_class():
    json = bottle.request.json
    token, req_teach, req_lec = json['token'], json['teacher'], json['lecture']
    status, message = tools.register_for_class_request(token,
                                                       req_teach, req_lec)
    return {'status': status, 'message': message}


@app.post('/user/request/approval')
def user_class_request_approval():
    json = bottle.request.json
    token = json['token']
    status, users = tools.get_pending_user_requests_to_join_class(token)
    return {'status': status, 'lectures': users}


@app.post('/user/request/approved')
def user_class_request_approved():
    json = bottle.request.json
    token, user, lecture = json['token'], json['user'], json['lecture']
    status = tools.approve_user(token, user, lecture)
    return {'status': status}


@app.get('/photos/<filename>')
def image_server(filename):
    with tools.Config() as config:
        root = config.C['directories']['photos']
    return bottle.static_file(filename, root=root)
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
