from behave import given, when, then
from shopping import app
from flask import g
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from setup_db import setup_database, import_data

@given('the server is running2')
def step_server_is_running(context):
    context.client = app.test_client()
    context.client.testing = True

@when('a visitor navigates to the book list page')
def step_navigate_to_book_list_page(context):
    context.response = context.client.get('/books')

@then('the book list page should load successfully')
def step_book_list_page_loads(context):
    assert context.response.status_code == 200

