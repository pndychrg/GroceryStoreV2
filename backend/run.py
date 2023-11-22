from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from extensions import db
from flask_cors import CORS
import workers
from celery.schedules import crontab
from lib.jobs.monthly_report import send_user_monthly_report
from lib.jobs.coupon_update import updateCoupons
app, celery = None, None


def create_app():
    # initialization
    app = Flask(__name__)
    app.secret_key = "21f1000649"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///groceryStoreV2.db'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
    db.init_app(app=app)

    # initializing api
    api = Api(app=app)
    jwt = JWTManager(app=app)
    app.config['JWT_SECRET_KEY'] = '21f1000649'
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # celery setup
    celery = workers.celery
    # updating the config
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
    )
    celery.conf.beat_schedule = {
        "trigger-monthly-report": {
            "task": "lib.jobs.monthly_report.send_user_monthly_report",
            "schedule": crontab(minute="0", hour="0", day_of_month="1")
        },
        "trigger-daily-coupon-update": {
            "task": "lib.jobs.coupon_update.updateCoupons",
            "schedule": crontab(day_of_week="*")
        },
    }
    celery.Task = workers.ContextTask

    app.app_context().push()
    # celery = workers.celery

    # boiler plate code for testing celery
    @app.route("/")
    def main():
        # send_user_monthly_report.delay()
        updateCoupons.delay()
        return "Hello world", 200

    # importing all api resources
    from lib.api.user import UserAPI
    from lib.api.sections import SectionAPI, GetAllSections, SectionRequestsAPI
    from lib.api.approve_managers import ApproveManagerAPI
    from lib.api.approve_sectionRequests import ApproveSectionRequests
    from lib.api.products import ProductsAPI
    from lib.api.products import ProductImage
    from lib.api.products import RecentProduct
    from lib.api.cart import CartAPI
    from lib.api.buy import BuyAPI
    from lib.api.search_products import SearchProductsAPI
    from lib.api.favourites import FavouritesAPI
    from lib.api.rating import RatingsAPI
    from lib.api.coupons import CouponAPI, CouponsExtendedAPI
    # registering all the api resources
    api.add_resource(UserAPI, '/user')
    api.add_resource(SectionAPI, '/section')
    api.add_resource(GetAllSections, '/sections')
    api.add_resource(ApproveManagerAPI, '/unapproved')
    api.add_resource(SectionRequestsAPI, '/section/request')
    api.add_resource(ApproveSectionRequests, '/section/approve')
    api.add_resource(ProductsAPI, '/product')
    api.add_resource(ProductImage, '/product/img')
    api.add_resource(RecentProduct, '/product/<limit>', endpoint='product')
    api.add_resource(CartAPI, '/cart')
    api.add_resource(BuyAPI, '/buy')
    api.add_resource(BuyAPI, '/buy/<coupon_id>', endpoint='buy')
    api.add_resource(SearchProductsAPI, '/product/search')
    api.add_resource(FavouritesAPI, '/product/favourite/<product_id>',
                     endpoint="favourite")
    api.add_resource(FavouritesAPI, '/product/favourite')
    api.add_resource(
        RatingsAPI, '/product/rating/<product_id>', endpoint='rating')
    api.add_resource(RatingsAPI, "/product/rating")
    api.add_resource(CouponAPI, '/coupon')
    api.add_resource(CouponAPI, '/coupon/<coupon_id>', endpoint='coupon')
    api.add_resource(CouponsExtendedAPI, '/coupons')
    api.add_resource(CouponsExtendedAPI,
                     "/coupons/<coupon_code>", endpoint="coupons")

    # registering the reports blueprint
    from lib.api.reports import report
    app.register_blueprint(report)
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
    return app, celery


def init_admin():
    # creating a defualt admin
    from models.user import User
    # check if admin exists
    if (User.query.filter_by(username='admin').first()):
        return 0
    admin = User(name='admin', username='admin',
                 password='admin', role='admin', email='admin@grocerystore.com')
    db.session.add(admin)
    db.session.commit()
    print(admin, flush=True)


app, celery = create_app()
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("create all func ran", flush=True)
        init_admin()
    app.run(debug=True, threaded=True)
