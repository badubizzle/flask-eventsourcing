from flask import Flask
import os

def create_app(config_override=None):    

    app = Flask(__name__)

    app.config.from_object('config.settings')

    if config_override:
        app.config.update(config_override)


    return app    


