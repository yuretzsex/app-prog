from flask import Flask, Response
from waitress import serve
from user import user, login
from announcement import announcement
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:1234@localhost/announcements'
app.register_blueprint(user)
app.register_blueprint(login)
app.register_blueprint(announcement)
app.config['JWT_SECRET_KEY'] = 'secret_key'
jwt = JWTManager(app)

serve(app, host='127.0.0.1', port=5000)