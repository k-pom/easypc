from flask import Flask
import os

app = Flask("easypc")
app.secret_key = os.environ.get('SECRET_KEY')

import easypc.login
import easypc.pcs
