from flask_bootstrap import Bootstrap
from easypc import app
from easypc.config import config


app.config.update(
    DEBUG=True,
    PROPAGATE_EXCEPTIONS=True
)

if __name__ == "__main__":
    Bootstrap(app)
    app.secret_key = config['app']['secret_key']
    app.run()
