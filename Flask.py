from flask import Flask
from flask import request
from flask import render_template
import DB_Util as dbu
import os

app = Flask(__name__)


# 普通路由
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/examples/<name>')
def show_example(name):
    return render_template('examples/' + name + '_example.html')


# 路由传参
# 使用模板
@app.route('/users/<name>')
def user(name):
    return render_template('user.html', name=name)


# 指定参数类型
@app.route('/articles/<string:article_name>')
def article(article_name):
    return 'article: ' + article_name


# 指定 HTTP Methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()


def do_the_login():
    pass


def show_the_login_form():
    pass


def init_database():
    if not os.path.exists(dbu.DATABASE):
        dbu.init_db(app)

if __name__ == '__main__':
    # init_database()
    app.run()
