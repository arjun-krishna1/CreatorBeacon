from qrcode import make
from time import time
import os, glob
from pathlib import Path

static_path = os.path.join(Path(__file__).parents[1], 'static')

def make_qr(data):
    code = make(data)
    name = str(time()) + ".png"
    code.save("static/" + name)
    return name

def make_website_link_qr(hash, time):
    return make_qr("http://127.0.0.1:8000/" + hash + time)

def delete_old_files():
    files = os.listdir(static_path)
    png_to_float = lambda file : float(file.replace(".png", ""))
    for file in files:
        if ".png" in file:
            time_change = time() - png_to_float(file)
            if time_change > 86400: # a day
                os.remove(os.path.join(static_path, file))





delete_old_files()