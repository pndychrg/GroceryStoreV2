from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from extensions import db
from flask_cors import CORS


def create_app():
    # initialization
    app = Flask(__name__)
    app.secret_key = "21f1000649"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///groceryStoreV2.db'
    db.init_app(app=app)

    # initializing api
    api = Api(app=app)
    jwt = JWTManager(app=app)
    app.config['JWT_SECRET_KEY'] = '21f1000649'
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # importing all api resources
    from lib.api.user import UserAPI

    # registering all the api resources
    api.add_resource(UserAPI, '/user')

    # api docs init code
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/docs/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test application"
        }
    )

    return app


def init_admin():
    # creating a defualt admin
    from models.user import User
    # check if admin exists
    if (User.query.filter_by(username='admin').first()):
        return 0
    admin = User(name='admin', username='admin',
                 password='admin', role='admin')
    db.session.add(admin)
    db.session.commit()
    print(admin, flush=True)


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        print("create all func ran", flush=True)
        init_admin()
    app.run(debug=True, threaded=True)
