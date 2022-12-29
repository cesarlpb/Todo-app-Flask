# my_app.py

from flask import Flask

app = Flask(__name__) # application 'app' is object of class 'Flask'

# import files
from test_routes import *


if __name__ == '__main__':
    # '0.0.0.0' = 127.0.0.1 i.e. localhost
    # port = 5000 : we can modify it for localhost
    app.run(host='0.0.0.0', port=5010, debug=True) # local webserver : app.run()