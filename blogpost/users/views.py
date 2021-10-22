# users/views.py
from flask import (
    render_template,
    url_for,
    redirect,
    flash,
    request,
    Blueprint)
from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required)
from blogpost.models import User, BlogPost
from blogpost.users.forms import (
    RegisterationForm,
    LoginForm,
    UpdateUserForm)
from blogpost.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data, password=form.password.data)
        user.save_to_db()
        flash('Thanks for registeration!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Log in Success!')
            next = request.args.get('next')  # 表示之前訪問的route
            if next == None or not next[0] == '/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.save_to_db()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',
                            filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html',
                           form=form,
                           profile_image=profile_image)


@users.route('/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.find_by_username_or_404(username)

    blog_posts = BlogPost.find_all_by_user(user, page, per_page=6)

    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
