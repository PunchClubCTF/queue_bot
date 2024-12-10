from flask import Blueprint, render_template
from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Add a new user (for testing)
    if not User.query.first():
        new_user = User(username="testuser", email="testuser@example.com")
        db.session.add(new_user)
        db.session.commit()

    users = User.query.all()
    return render_template('index.html', users=users)
