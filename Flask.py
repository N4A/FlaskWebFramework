from flask import Flask
from flask import request
from flask import render_template
from flask import g
import DB_Util as dbu
from domain.user import User

app = Flask(__name__)


# 普通路由
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/examples/<name>')
def show_example(name):
    return render_template('examples/' + name + '_example.html')


# 路由传参
# 使用模板, 模板传参
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


@app.route('/search', methods=['POST'])
def search():
    return 'key word: ' + request.form.get('search_key') + '<br> Find nothing.'


def do_the_login():
    pass


def do_the_register():
    name = request.form.get('name')
    passwd = request.form.get('passwd')
    g.db.add(User(name=name, passwd=passwd))
    g.db.commit()


def show_the_login_form():
    pass


@app.before_request
def before_request():
    g.db = dbu.get_sesion()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == '__main__':
    app.run(port=5001)
