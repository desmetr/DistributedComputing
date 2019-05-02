import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    STATIC_PATH_PHOTO = "/src/photo/static"
    # STATIC_PATH_PHOTO = "/" + basedir + "/../photo/static"