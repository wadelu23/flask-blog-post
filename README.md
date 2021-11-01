# Flask Blog Post
> 簡易Blog Post站
> 
> 功能:
> * 登入、註冊、編輯個人資料、上傳個人頭像
> * 新增修改刪除貼文(貼文內容為markdown格式)
> * 使用者主頁，瀏覽該使用者所有貼文

[展示站](https://flask-simple-blog-posts.herokuapp.com/)(於heroku)

---

- [Flask Blog Post](#flask-blog-post)
  - [使用Package](#使用package)
  - [本地建置步驟](#本地建置步驟)
  - [Heroku部署](#heroku部署)
  - [筆記](#筆記)
    - [Blueprint](#blueprint)
      - [切分方式](#切分方式)
    - [FlaskForm](#flaskform)
    - [templates(Jinja2)](#templatesjinja2)
      - [Template Inheritance](#template-inheritance)
    - [db migrate](#db-migrate)

---

## 使用Package
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/0.15.x/quickstart/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [Werkzeug](https://werkzeug.palletsprojects.com/en/2.0.x/)

---

## 本地建置步驟
1. clone 此專案，並進入資料夾
2. 安裝所需package，`pip install -r requirements.txt` 
   * 建議安裝在虛擬環境，可利用Anaconda、Miniconda或Venv
3. 執行 `flask db upgrade`，建立sqlite資料庫
4. 執行 `python app.py`，運行Flask
5. 打開瀏覽器輸入網址 http://127.0.0.1:5000/

## Heroku部署
1. 在Heroku建立新app
2. connect git remote(可與你的github repo連結)
3. 注意app的Settings裡，Config Vars需設定FLASK_ENV為production
   * 此變數是用來切換設定檔，如沒設定則預設為開發用的設定檔

4. 在app中，添加add-ons，以`Heroku Postgres`作為資料庫
5. 可設定自動部署，搭配 Procfile 中的`release: flask db upgrade`，如有變更資料庫結構即可部署時自動更新資料庫

---

## 筆記
### Blueprint
此處簡略紀錄，如需要更詳細的說明可參考

[Python Web Flask — Blueprints 解決大架構的網站](https://medium.com/seaniap/python-web-flask-blueprints-%E8%A7%A3%E6%B1%BA%E5%A4%A7%E6%9E%B6%E6%A7%8B%E7%9A%84%E7%B6%B2%E7%AB%99-1f9878312526)

或官方文件
[Blueprints and Views](https://flask.palletsprojects.com/en/2.0.x/tutorial/views/)

以及
[Use a Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/#what-a-flask-application-looks-like)


```python
# blogpost/core/views.py
from flask import Blueprint
# 定義blueprint
core = Blueprint('core', __name__)

# 定義route
@core.route('/')
def index():
   return render_template('index.html')
@core.route('/info')
def index():
   return render_template('info.html')

```

```python
# Import and register Blueprint
# blogpost/__init__.py
from flask import Flask
from blogpost.core.views import core

app = Flask(__name__)

app.register_blueprint(core)

```

#### 切分方式
1. 以路徑分 (本專案目前切分方式)
   * 切分route，而樣板統一放在主要資料夾templates內。
2. 以功能分
   * 根據功能建立路徑，並且有專屬的樣板資料夾

```python
# 以功能分 的 範例
ecommerce/
|
├── auth/
|   ├── templates/
|   |   └── auth/
|   |       ├── login.html
|   |       ├── forgot_password.html
|   |       └── signup.html
|   |
|   ├── __init__.py
|   └── auth.py
|
├── cart/
|   ├── templates/
|   |   └── cart/
|   |       ├── checkout.html
|   |       └── view.html
|   |
|   ├── __init__.py
|   └── cart.py
|
├── products/
|   ├── static/
|   |   └── view.js
|   |
|   ├── templates/
|   |   └── products/
|   |       ├── list.html
|   |       └── view.html
|   |
|   ├── __init__.py
|   └── products.py
```

```python
# products的templates中多一層products
# 可用來避免 template name collisions
ecommerce/
|
└── products/
    └── templates/
        └── products/
            ├── search.html
            └── view.html
```

---

### FlaskForm
```python
# Creating Forms
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField)
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Post')
```

Route 傳遞或驗證 Forms
```python
from flask import (
    render_template,
    url_for,
    redirect,)

@blog_posts.route('/create', methods=['GET', 'POST'])
def create_post():
   form = BlogPostForm()
   if form.validate_on_submit():
      # 省略...
      return redirect(url_for('core.index'))

   return render_template('create_post.html', form=form)
```

渲染HTML，只列出form範圍，其他省略
```html
<form method="POST" action="/">
    {{ form.csrf_token }}
    {{ form.title.label }} {{ form.title }}
    {{ form.text.label }} {{ form.text }}
    {{ form.submit() }}
</form>
```

---

### templates([Jinja2](https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance))

```python
from flask import render_template

# 使用render_template渲染頁面
@core.route('/info')
def info():
    return render_template('info.html')
   # 也可傳參數至頁面顯示
   # title = "Info !!"
   # return render_template('info.html',title=title)
```

#### Template Inheritance

[Base / Child Template](https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance)

Base Template
```html
<!DOCTYPE html>
<html lang="en">
<head>
    {% block head %}
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}{% endblock %} - My Webpage</title>
    {% endblock %}
</head>
<body>
    <div id="content">{% block content %}{% endblock %}</div>
</body>
</html>
```

Child Template
```html
{% extends "base.html" %}
{% block title %}Index{% endblock %}
{% block head %}
    {{ super() }}
    <style type="text/css">
        .important { color: #336699; }
    </style>
{% endblock %}
{% block content %}
    <h1>Index</h1>
    <p class="important">
      Welcome to my awesome homepage.
    </p>
{% endblock %}
```

Macros (類似於函數，可重複利用)
```html
{% macro input(name, value='', type='text', size=20) -%}
    <input type="{{ type }}" name="{{ name }}" value="{{
        value|e }}" size="{{ size }}">
{%- endmacro %}
```

使用Macros
```html
<p>{{ input('username') }}</p>
<p>{{ input('password', type='password') }}</p>
```

可利用Pagination物件的屬性來自訂換頁按鈕樣式

[flask_sqlalchemy.Pagination](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.Pagination)


範例
```html
  <div class=pagination>
  {%- for page in pagination.iter_pages() %}
    {% if page %}
      {% if page != pagination.page %}
        <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
      {% else %}
        <strong>{{ page }}</strong>
      {% endif %}
    {% else %}
      <span class=ellipsis>…</span>
    {% endif %}
  {%- endfor %}
  </div>
```

---

### db migrate
```python
# 如果flask主入口檔名為app.py就不用此額外設定
export FLASK_APP=myapp.py

# Sets up the migrations directory
flask db init

# generate migration
flask db migrate -m "some message"

# apply the migration to the database
flask db upgrade

```