from flask import Flask

from app_prog.user import user, login
from app_prog.announcement import announcement
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:12345@localhost/aplabs"
app.config["JWT_SECRET_KEY"] = "love"
jwt = JWTManager(app)
app.register_blueprint(user)
app.register_blueprint(announcement)
app.register_blueprint(login)

@app.route('/api/v1/hello-world-3')
def hello_world():
    return 'Hello World 3'
