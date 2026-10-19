from flask import Flask
from app import models

app = Flask(__name__, template_folder='app/templates', static_folder='app/static', static_url_path='/')

import app.routes as routes


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 