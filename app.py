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

server = secure.Server().set("Secure")

csp = (
    secure.ContentSecurityPolicy()
    .default_src("'none'")
    .base_uri("'self'")
    .connect_src("'self'" "api.spam.com")
    .frame_src("'none'")
    .img_src("'self'", "static.spam.com")
)

if os.environ.get('ENVIRONMENTPROD'):
    hsts = secure.StrictTransportSecurity().include_subdomains().preload().max_age(2592000)
    print(os.environ.get('ENVIRONMENTPROD'))

referrer = secure.ReferrerPolicy().no_referrer()

permissions_value = (
    secure.PermissionsPolicy().geolocation("self", "'spam.com'").vibrate()
)

cache_value = secure.CacheControl().must_revalidate()

if os.environ.get('ENVIRONMENTPROD'):
    secure_headers = secure.Secure(
    server=server,
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    permissions=permissions_value,
    cache=cache_value,
    )
else:
    secure_headers = secure.Secure(
    server=server,
    csp=csp,
    referrer=referrer,
    permissions=permissions_value,
    cache=cache_value,
    )

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = postgresqlConfig
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')

jwt = JWTManager(app)
api = Api(app)

SELF = "'self'"
talisman = Talisman(
    app,
    content_security_policy={
        'default-src': SELF,
        'img-src': '*',
        'script-src': [
            SELF,
            'some.cdn.com',
        ],
        'style-src': [
            SELF,
            'another.cdn.com',
        ],
    },
    content_security_policy_nonce_in=['script-src'],
    feature_policy={
        'geolocation': '\'none\'',
    }
)

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

async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.flask(response)
    return response

if __name__ == '__main__':
    app.run(debug=True) 
