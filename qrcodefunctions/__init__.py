from qrcode import make
from time import time
import os
from pathlib import Path

static_path = os.path.join(Path(__file__).parents[1], 'static')

def make_qr(data):
    code = make(data)
    name = str(time()) + ".png"
    code.save("static/" + name)
    return name

def make_website_link_qr(hash):
    return make_qr("http://127.0.0.1:8000/" + hash + "/qr")