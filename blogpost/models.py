from blogpost.db import db
from blogpost.login_manager import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from typing import Optional


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class CommonQuery():
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, UserMixin, CommonQuery):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(
        db.String(50), nullable=False, default='default_profile.png')
    email = db.Column(db.String(50), unique=True, index=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username} "

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_username_or_404(cls, username):
        return cls.query.filter_by(username=username).first_or_404()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


class BlogPost(db.Model, CommonQuery):
    per_page = 10

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id}, Date: {self.date}, Title:{self.title}"

    @classmethod
    def find_all_by_user(cls, user: User,  page: int, per_page: Optional[int] = per_page, date_order: Optional[str] = 'desc') -> list["BlogPost"]:
        """find all post from the user with date order and pagination

        Args:
            user (User): [User Model]
            page (int): [current page]
            per_page (Optional[int], optional): [per_page Number].Defaults to 10.
            date_order (Optional[str], optional): [date order rule]. Defaults to 'desc'.

        Returns:
            list: [BlogPost]
        """

        date_order_rule = cls.date.desc() if date_order == 'desc' else cls.date.asc()

        blog_posts = cls.query.filter_by(author=user).order_by(
            date_order_rule).paginate(page=page, per_page=per_page)
        return blog_posts

    @classmethod
    def find_all(cls, page: int, per_page: Optional[int] = per_page):
        return cls.query.order_by(
            cls.date.desc()).paginate(page=page, per_page=per_page)
