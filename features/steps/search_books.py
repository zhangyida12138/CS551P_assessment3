from behave import given, when, then
from shopping import app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from setup_db import setup_database, import_data

@given('the server is running5')
def step_server_is_running(context):
    context.client = app.test_client()
    context.client.testing = True

@when('a visitor searches for a keyword')
def step_visitor_searches_for_keyword(context):
    context.response = context.client.get('/search?query=the')

@then('the search results should display all books matching the keyword')
def step_search_results_display(context):
    pass