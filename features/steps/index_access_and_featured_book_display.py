from behave import given, when, then
from shopping import app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from setup_db import setup_database, import_data


@given('the server is running10')
def step_server_is_running(context):
    context.client = app.test_client()
    context.client.testing = True

@when('a visitor navigates to the home page')
def navigate_to_home_page(context):
    context.response = app.test_client().get('/')

@then('the home page should load successfully')
def home_page_loads_successfully(context):
    assert context.response.status_code == 200

@then('a list of featured books should be displayed')
def featured_books_displayed(context):
    assert b'Recommended Books' in context.response.data
    assert b'class="card-title"' in context.response.data
    assert b'class="card-text">author:' in context.response.data
    assert b'class="card-text">price:' in context.response.data
    assert b'class="btn btn-primary">view detail' in context.response.data