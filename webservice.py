import os
import tools
import bottle

TEMPLATES = 'templates'
CLASS_PHOTOS = 'photos'


def render(template, data=None):
    data = data if data is not None else dict()
    with open(os.path.join(TEMPLATES, template)) as fl:
        html = fl.read()
    return bottle.template(html, **data)


app = bottle.Bottle()


@app.get('/')
def home():
    return render('home.html')


@app.post('/newimage/')
def newimage():
    image = bottle.request.files.get('classphoto')
    image.save(os.path.join(CLASS_PHOTOS, image.filename))
    return {'saved': True}


@app.get('/label/')
def get_attendance():
    images = os.listdir(CLASS_PHOTOS)
    names = [tools.get_names(i) for i in images]
    return {'images': images, 'names': names}


@app.get('/static/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='static')
