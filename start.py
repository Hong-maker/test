from flask import Flask

# Flask类的实例化将会是我们的 WSGI 应用
# __name__模块名称，这样 Flask 才会知道去哪里寻找模板、静态文件等等。
app = Flask(__name__)


# 装饰器route添加路由，告诉 Flask 哪个 URL 才能触发我们的函数。
@app.route('/')
def hello_world():
    return 'Hello'

if __name__ == '__main__':
    # 启动本地服务器
    app.run()