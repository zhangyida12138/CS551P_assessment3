from behave import given, when, then
from shopping import app
import sys
import os
from flask import url_for,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from setup_db import setup_database, import_data


@given('a user is logged in')
def user_logged_in(context):
    context.client = app.test_client()
    with context.client:
        response = context.client.post('/login', data=dict(
            username='123456',
            password='123456'
        ), follow_redirects=True)

@when('the user logs out')
def user_logs_out(context):
    context.response = app.test_client().get('/logout', follow_redirects=True)

@then('the user should be logged out successfully')
def step_user_redirected_to_home_page(context):
    pass