import os
from easypc import app


app.config.update(
    DEBUG=True,
    PROPAGATE_EXCEPTIONS=True
)

if __name__ == "__main__":
    app.secret_key = os.environ.get('SECRET_KEY')
    app.run()
