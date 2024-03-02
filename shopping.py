import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

# database details - to remove some duplication
db_name = 'shopping_data.db'

@app.route('/')
def index():

    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # get results from customers
    cur.execute("select * from customers")
    customers = cur.fetchall()

    # get results from orders for each customer id
    cust_order=dict()
    for customer in customers:
        cur.execute("select Count(*) from orders WHERE customer_id=?", (customer[0],))
        num = cur.fetchone()
        cust_order[customer["name"]]=num[0]

    conn.close()
    return render_template('index.html', cust_order=cust_order)

@app.route('/customers')
def customers():
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # get results from customers
    cur.execute("select * from customers")
    rows = cur.fetchall()
    conn.close()
    return render_template('customers.html', rows=rows)

@app.route('/customer_details/<id>')
def customer_details(id):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # get results from customers
    cur.execute("select * from customers WHERE id=?", (id,))# do not forget the comma which makes the parameter a tuple
    customer = cur.fetchall()
    # get results from orders for this customer id
    cur.execute("select * from orders WHERE customer_id=?", (id,))
    orders = cur.fetchall()

    conn.close()
    return render_template('customer_details.html', customer=customer, orders=orders)

@app.route('/orders')
def orders():
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # get results from orders
    cur.execute("select * from orders")
    rows = cur.fetchall()
    conn.close()
    return render_template('orders.html', rows=rows)

@app.route('/order_details/<id>')
def order_details(id):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # get results from orders
    cur.execute("select * from orders WHERE id=?", (id,))
    order = cur.fetchall()

    customer_id=order[0]["customer_id"]
    # get results from customers for this order
    cur.execute("select * from customers WHERE id=?", (customer_id,))
    customer = cur.fetchall()

    # get results from line_items
    cur.execute("select * from line_items WHERE order_id=?", (id,))
    items = cur.fetchall()

    conn.close()
    return render_template('order_details.html', order=order, customer=customer, items=items)