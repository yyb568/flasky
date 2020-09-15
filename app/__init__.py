# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config

# 创建数据库
db = SQLAlchemy()

def create_app(config_name):

    # 初始化
    app = Flask(__name__)

    # 导致指定的配置对象:创建app时，传入环境的名称
    app.config.from_object(config[config_name])

    # 初始化扩展（数据库）
    db.init_app(app)

    # 创建数据库表
    create_tables(app)

    # 注册所有蓝本
    regist_blueprints(app)

    return app

def regist_blueprints(app):

    # 导入蓝本对象
    # 方式一
    from app.api import api

    # 方式二：这样，就不用在app/api/__init__.py（创建蓝本时）里面的最下方单独引入各个视图模块了
    # from app.api.views import api
    # from app.api.errors import api

    # 注册api蓝本,url_prefix为所有路由默认加上的前缀
    app.register_blueprint(api, url_prefix='/api')

def create_tables(app):
    """
    根据模型，创建表格（可以有两种写法）
    1、模型必须在create_all方法之前导入，模型类声明后会注册到db.Model.metadata.tables属性中
    不导入模型模块，就不会执行模型中的代码，也就无法完成注册。
    2、但是，如果db是在模型模块中创建的，同时在此处 from app.models import db 引用db,则就实现了
    模型和数据库的绑定，不需要再单独导入模型模块了。
    """
    from app.models import Video
    db.create_all(app=app)