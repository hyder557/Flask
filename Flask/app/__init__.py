# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .predict.train import initialize_model
from config import Config
from flask_cors import CORS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='./login/templates',
                static_folder='./login/static')
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    with app.app_context():
        initialize_model()

    from .login.routes import main as login_main_blueprint
    from .userManage.userManage import user_manager
    from .goodsManage.goodsManage import goods_manager
    from .demandsManage.demandManage import demand_manager
    from .caseManage.caseManage import case_manager
    from .predict.predict import prediction
    from .taskManage.taskManage import task

    app.register_blueprint(login_main_blueprint)
    app.register_blueprint(user_manager)
    app.register_blueprint(goods_manager)
    app.register_blueprint(demand_manager)
    app.register_blueprint(case_manager)
    app.register_blueprint(prediction)
    app.register_blueprint(task)

    return app
