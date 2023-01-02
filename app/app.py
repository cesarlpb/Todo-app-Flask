# save this as app.py
from flask import Flask

app = Flask(__name__)

# import files
from routes import *

# 5000 - cambiar puerto a uno que esté libre
if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5019, debug = True)