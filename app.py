from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_talisman import Talisman
from resources.information import Information, InformationList, InformationById
from resources.user import UserRegister, User
from config import postgresqlConfig
import secure
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = postgresqlConfig
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')

jwt = JWTManager(app)
api = Api(app)

@app.before_first_request
def create_tables():
    from db import db
    db.init_app(app)
    db.create_all()

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user')
api.add_resource(Information, '/information')
api.add_resource(InformationById, '/information/<int:id>')
api.add_resource(InformationList, '/infomationlist')

if __name__ == '__main__':
    app.run(debug=True) 
