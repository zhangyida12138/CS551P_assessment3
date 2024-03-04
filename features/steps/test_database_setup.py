from behave import given, when, then
import sqlite3
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from setup_db import setup_database, import_data


@given('has created an empty SQLite database')
def step_impl(context):
    context.db_path = 'features/steps/test_shopping_data.db'
    if os.path.exists(context.db_path):
        os.remove(context.db_path)
    context.conn = sqlite3.connect(context.db_path)
    context.cursor = context.conn.cursor()

@when('executing database creation and data import scripts')
def step_impl(context):
    setup_database(context.cursor)
    import_data(context.cursor, 'csv/bookdata.csv')
    context.conn.commit()

@then('the database should contain the correct table structure')
def step_impl(context):
    tables = ["authors", "categories", "books", "users"]
    for table in tables:
        context.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
        result = context.cursor.fetchone()
        assert result is not None, f"Table {table} does not exist."

@then('should successfully import the specified number of records into each table')
def step_impl(context):
    # Have at least one record in each table
    tables = ["authors", "categories", "books"]
    for table in tables:
        context.cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = context.cursor.fetchone()[0]
        assert count > 0, f"Table {table} has no records."
