from behave import given, when, then
from shopping import app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from setup_db import setup_database, import_data

@given('the server is running3')
def step_server_is_running(context):
    context.client = app.test_client()
    context.client.testing = True

@when('a visitor navigates to a non-existent page')
def step_visitor_navigates_to_non_existent_page(context):
    context.response = context.client.get('/some_non_existent_page')

@then('a custom 404 error page should be displayed')
def step_custom_404_page_displayed(context):
    assert context.response.status_code == 404
    assert 'Page Not Found' in context.response.get_data(as_text=True)

@when('an internal server error occurs')
def step_internal_server_error_occurs(context):
    context.response = context.client.get('/test-500')

@then('a custom 500 error page should be displayed')
def step_custom_500_page_displayed(context):
    assert context.response.status_code == 500
    assert 'Internal Server Error' in context.response.get_data(as_text=True)