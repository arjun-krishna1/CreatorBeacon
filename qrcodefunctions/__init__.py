from qrcode import make
from time import time
import os
from pathlib import Path

static_path = os.path.join(Path(__file__).parents[1], 'static')


def make_qr(data, name):
    code = make(data)
    name = str(name) + ".png"
    code.save(os.path.join(static_path, name))
    return name

def make_website_link_qr(id):
    return make_qr("http://127.0.0.1:8000/enterEvent/" + str(id), id)
