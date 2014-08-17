from flask import Flask
app = Flask("easypc")
app.secret_key=os.environ.get('SECRET_KEY')

import easypc.login
import easypc.pcs
