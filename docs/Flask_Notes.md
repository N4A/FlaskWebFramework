# Flask +jinja2+bootstrap+sqlite3+sqlalchemy构建web基础学习总结

## 1 route 路由

1. 语法

```python
# 普通路由
@app.route('/')
def index():
    return 'Hello World!!!'


# 路由传参
@app.route('/users/<name>')
def user(name):
    return 'user: ' + name


# 指定参数类型， 参考下面2
@app.route('/articles/<string:article_name>')
def article(article_name):
    return 'article: ' + article_name


# 指定 HTTP Methods  参考下面3
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()
        
# 获取表单数据
@app.route('/search', methods=['POST'])
def search():
    return 'key word: ' + request.form.get('search_key') + '<br> Find nothing.'
```

2. The following converters exist:

| string | accepts any text without a slash (the default) |
| ------ | ---------------------------------------- |
| int    | accepts integers                         |
| float  | like `int` but for floating point values |
| path   | like the default but also accepts slashes |
| any    | matches one of the items provided        |
| uuid   | accepts UUID strings                     |

3. Http Methods

   `GET`

   The browser tells the server to just *get* the information stored on that page and send it. This is probably the most common method.

   `HEAD`

   The browser tells the server to get the information, but it is only interested in the *headers*, not the content of the page. An application is supposed to handle that as if a `GET` request was received but to not deliver the actual content. In Flask you don’t have to deal with that at all, the underlying Werkzeug library handles that for you.

   `POST`

   The browser tells the server that it wants to *post* some new information to that URL and that the server must ensure the data is stored and only stored once. This is how HTML forms usually transmit data to the server.

   `PUT`

   Similar to `POST` but the server might trigger the store procedure multiple times by overwriting the old values more than once. Now you might be asking why this is useful, but there are some good reasons to do it this way. Consider that the connection is lost during transmission: in this situation a system between the browser and the server might receive the request safely a second time without breaking things. With `POST` that would not be possible because it must only be triggered once.

   `DELETE`

   Remove the information at the given location.

   `OPTIONS`

   Provides a quick way for a client to figure out which methods are supported by this URL. Starting with Flask 0.6, this is implemented for you automatically.

## 2 static: 通过url直接访问静态文件

静态文件直接放在static目录下，通过url: **static/<filename>**即可访问

## 3 templates: 使用模板，模板语法参考jinja2

1. base template: 申明block，子模版可以通过block复写父模板对应block下的内容，如下

   ```html

   <!doctype html>
   <html>
     <head>
       {% block head %}
           <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
           <link rel="stylesheet" href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css">
           <script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
           <script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
   {#        title block#}
           <title>{% block title %}{% endblock %}</title>
       {% endblock %}
     </head>
     <body>

   {#    navigation bar#}
       <div id="nav">{% block nav %} {% endblock %}</div>

   {#    main content block#}
       <div id="content">{% block content %}{% endblock %}</div>

   {#    footer block#}
       <div id="footer" class="bottom footer text-center">
         {% block footer %}
           <br><br>
           <h3>&copy; Copyright 2017 by <a href="http://www.github.com/N4A/">N4A</a>.</h3>
         {% endblock %}
       </div>

     </body>
   </html>
   ```

   该模板将页面大致分为几个区域，确定了页面的整体框架。

2. 子模版：static_nav_bar.html

   ```html
   {% extends "layout/base.html" %}
   {% block title %}static nav bar{% endblock %}

   {% block nav %}

       <nav class="navbar navbar-default navbar-static-top">
         <div class="container-fluid">
           <!-- Brand and toggle get grouped for better mobile display -->
           <div class="navbar-header">
             <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
               <span class="sr-only">Toggle navigation</span>
               <span class="icon-bar"></span>
               <span class="icon-bar"></span>
               <span class="icon-bar"></span>
             </button>
             <a class="navbar-brand" href="/">Home</a>
           </div>

           <!-- Collect the nav links, forms, and other content for toggling -->
           <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
               {% block nav_content %}

               {% endblock %}
           </div><!-- /.navbar-collapse -->
         </div><!-- /.container-fluid -->
       </nav>

   {% endblock %}
   ```

   注意该模板继承上面的模板，复写了{% block nav %}块，确定navigation bar的样式，并且留出{% block nav_content %}供使用者决定内容。这样我们就可以确定一个基本的带响应式导航栏的页面样式。而他们就可以不断被复用。下面是一个列子。

3. my_nav_bar.html

   ```html
   {% extends 'layout/static_nav_bar.html' %}

   {% block nav_content %}
        <ul class="nav navbar-nav">
           <li><a href="https://github.com/N4A/FlaskWebFramework/tree/master/docs">Documentation</a></li>
           <li><a href="https://github.com/N4A/FlaskWebFramework">Download</a></li>
           <li class="dropdown">
             <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
                 Bootstrap Examples
             <span class="caret"></span></a>
             <ul class="dropdown-menu">
               <li><a href="/examples/grid">Grid Example</a></li>
               <li><a href="/examples/theme">Theme Example</a></li>
             </ul>
           </li>
        </ul>
         <form action="/search" method="post" class="navbar-form navbar-right">
           <div class="form-group">
             <input type="text" name="search_key" class="form-control" placeholder="Search">
           </div>
           <button type="submit" class="btn btn-default">Submit</button>
         </form>
   {% endblock %}
   ```

   该模板继承上面的模板，确定了一个具体的导航栏。

## 4 使用sqllite3

```python
import sqlite3
from flask import g
import os

DATABASE = '/path/to/database.db'

def connect_db():
	# 这里使用相对路径可能会失效，虽然是官网样例，我试验的时候就失败了
    # return sqlite3.connect(DATABASE)
    # 使用绝对路径
	PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))#当前文件目录
	AB_DATABASE = os.path.join(PROJECT_ROOT, DATABASE)
    return sqlite3.connect(DATABASE)
  
    
# 该函数会在一个请求开始前执行，
# 这样在任何一个请求里都可以直接使用g.db访问数据库
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
```

## 5 使用ORM框架： SQLAlchemy

[参考连接](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0014021031294178f993c85204e4d1b81ab032070641ce5000)

1. 声明model

   ```python
   #!/usr/bin/env python
   # -*- coding: utf-8 -*-
   # @Time    : 2017/5/28 13:05
   # @Author  : duocai

   # 导入:
   from sqlalchemy import Column, String
   from sqlalchemy.ext.declarative import declarative_base

   # 创建对象的基类:
   Base = declarative_base()


   # 定义User对象:
   class User(Base):
       # 表的名字:
       __tablename__ = 'users'

       # 表的结构:
       id = Column(String(20), primary_key=True)
       name = Column(String(20))
       passwd = Column(String(20))
   ```

2. 使用SQLAlchemy连接数据库和使用

   ```python
   ## dbu.py
   def get_sesion(url=sqlalchemy_db):
       # 初始化数据库连接:
       engine = create_engine(url)
       # 创建DBSession类型:
       return sessionmaker(bind=engine)()


   # test db
   if __name__ == '__main__':
       # init_db,!!!!! delete the old one and create the new one
       init_db() ##这里就创建一个数据库，详见下面源码
       print('create db: ok')
       # test sqlalchemy
       sess = get_sesion()
       sess.add(User(id=1, name='Test', passwd='Test'))
       sess.commit()
       print('test insert user(name=Test, passwd=Test): ok')

       user = sess.query(User).one()
       print('test reading user from the database: ')
       print('user: ', user)
       print('print message of the user: ')
       print('name: ', user.name, ', passwd', user.passwd)
       sess.close()
       print('The database works well.')
   ```

3. 在flask里使用

   ```python
   ## improt dbu
   @app.before_request
   def before_request():
       g.db = dbu.get_sesion()


   @app.teardown_request
   def teardown_request(exception):
       if hasattr(g, 'db'):
           g.db.close()
   ```

## 总结：

1. [source codes](https://github.com/N4A/FlaskWebFramework)
2. [样例演示](http://120.76.125.35:5001)

