from behave import given, when, then,use_step_matcher
from shopping import app
from flask import url_for
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from setup_db import setup_database, import_data

use_step_matcher("re")

@given('the server is running1')
def step_impl(context):
    context.client = app.test_client()
    context.client.testing = True

@when('a visitor navigates to a specific book detail page with ASIN "([^"]+)"')
def navigate_to_book_detail_page(context, asin):
    context.response = app.test_client().get(f'/book/{asin}')
    
@then('the book detail page should load successfully')
def step_impl(context):
    assert context.response.status_code == 200

@then('the visitor should see the details of the book')
def step_impl(context):
    data = context.response.get_data(as_text=True)
    assert 'class="img-fluid"' in data
    assert '<h2>' in data
    assert '<strong>author:</strong>' in data
    assert '<strong>price:</strong>' in data
    assert '<strong>star:</strong>' in data
    assert '<strong>publishedDate:</strong>' in data
    # Checking for optional content
    if 'best selling books' in data:
        assert '<span class="badge bg-success">best selling books</span>' in data
    if 'editors pick' in data:
        assert '<span class="badge bg-info">editors pick</span>' in data
    if 'good reads choice' in data:
        assert '<span class="badge bg-warning">good reads choice</span>' in data
    # Check for the presence of the buy button with the correct link
    assert 'btn btn-primary' in data
    assert 'buy this book' in data