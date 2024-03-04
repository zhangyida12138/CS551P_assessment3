from behave import given, when, then
from shopping import app
import sys
import os
from flask import url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from setup_db import setup_database, import_data

@given('the server is running8')
def step_server_is_running(context):
    context.client = app.test_client()
    context.client.testing = True

@when('a visitor registers with a username and password')
def step_visitor_registers(context):
    # Use context.client to send a POST request to register a new user
    context.response = context.client.post('/register', data={
        'username': '456',
        'password': '456'
    }, follow_redirects=True)

@then('the user should be redirected to the login page')
def step_user_redirected_to_login_page(context):
    pass