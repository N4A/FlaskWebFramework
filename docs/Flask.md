Flask

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

## 3 templates: 使用模板

