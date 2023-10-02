from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from extensions import db
from models.roles import Role
from flask_cors import CORS

def create_app():
    # initialization
    app = Flask(__name__)
    app.secret_key = "21f1000649"
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///groceryStoreV2.db'
    db.init_app(app=app)

    # initializing api
    api = Api(app=app)
    jwt = JWTManager(app=app)
    app.config['JWT_SECRET_KEY']='21f1000649'
    cors = CORS(app,resources={r"/*":{"origins":"*"}})

    # importing all api resources
    from lib.api.user import UserAPI

    # registering all the api resources
    api.add_resource(UserAPI,'/user')


    # api docs init code
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/docs/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name':"Test application"
        }
    )

    return app

# Function to initialize the roles in the application
def init_roles():
    print("roles created",flush=True)
    with app.app_context():
        # create the user role if it doesn't exist
        user_role = Role.query.filter_by(name='user').first()
        if user_role is None:
            user_role = Role(name="user")
            db.session.add(user_role)
        
        # create the manager role
        manager_role = Role.query.filter_by(name="manager").first()
        if manager_role is None:
            manager_role = Role(name="manager")
            db.session.add(manager_role)

        # create the admin role
        admin_role = Role.query.filter_by(name="admin").first()
        if admin_role is None:
            admin_role = Role(name="admin")
            db.session.add(admin_role)
        db.session.commit()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        print("create all func ran",flush=True)
        init_roles()
    app.run(debug=True,threaded=True)