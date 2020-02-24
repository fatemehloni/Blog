from flask import Flask
from mod_Admin import admin

app = Flask(__name__)


@app.route('/')
def index():
    return 'Blog Home !'

app.register_blueprint(admin)

if __name__ == '__main__':
    app.run()
