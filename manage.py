# -*- coding: utf-8 -*-

# 启动程序
from app import create_app

"""
development:    开发环境
production:     生产环境
testing:        测试环境
default:        默认环境

"""
# 通过传入当前的开发环境，创建应用实例，不同的开发环境配置有不同的config。这个参数也可以从环境变量中获取
app = create_app('production')

if __name__ == '__main__':
    # flask内部自带的web服务器，只可以在测试时使用
    # 应用启动后，在9001端口监听所有地址的请求，同时根据配置文件中的DEBUG字段，设置flask是否开启debug
    app.run(host='127.0.0.1', port=9001, debug=app.config['DEBUG'])