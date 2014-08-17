from flask import Flask
app = Flask("easypc")
app.secret_key="JFKDJFDK"

import easypc.login
import easypc.pcs
