from behave import given, when, then
from shopping import app
import sys
import os
from flask import url_for,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from setup_db import setup_database, import_data

@given('the server is running6')
def step_server_is_running(context):
    context.client = app.test_client()
    context.client.testing = True

@given('a user has already registered')
def user_registered(context):
    pass

@when('the user logs in with correct credentials')
def step_user_logs_in_with_correct_credentials(context):
    context.response = context.client.post('/login', data=dict(
        username='123456',
        password='123456'
    ), follow_redirects=True)
    # assert 'id' in session#make sure the session now has 'id' indicating a logged-in user

@then('the user should be logged in successfully')
def step_user_redirected_to_home_page(context):
    pass

@then('redirected to the home page1')
def step_redirected_to_home_page(context):
    pass