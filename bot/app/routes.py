from flask import Blueprint, render_template
import json
from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('index.html')

@main.route('/get_queue')
def profile():
    return json.load()

@main.route('/add_user_to_queue')
def profile():
    return render_template('index.html')

@main.route('/delete_user_from_queue')
def profile():
    return render_template('index.html')



admin = Blueprint('admin', __name__)

@admin.route('/')
def profile():
    return render_template('index.html')

@admin.route('/add_lab')
def profile():
    return render_template('index.html')

@admin.route('/delete_lab')
def profile():
    return render_template('index.html')


