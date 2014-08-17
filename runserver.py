from easypc import app
from easypc.config import config


app.config.update(
    DEBUG=True,
    PROPAGATE_EXCEPTIONS=True
)

if __name__ == "__main__":
    app.secret_key = config['app']['secret_key']
    app.run()
