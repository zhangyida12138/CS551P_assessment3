from flask import Flask, render_template, g

app = Flask(__name__)

DATABASE = 'shopping_data.db'

def get_db_connection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.asin, b.title, a.name as author, b.imgUrl, b.productURL, b.price
            FROM books b
            JOIN authors a ON b.author_id = a.author_id
            WHERE b.isBestSeller = 1
            LIMIT 10;
        ''')
        featured_books = cursor.fetchall()
        return render_template('index.html', featured_books=featured_books)
    except sqlite3.DatabaseError as error:
        print(f"Database error: {error}")
        return "A database error occurred.", 500
    finally:
        if conn:
            conn.close()

            
# @app.route('/customers')
# def customers():
#     conn = sqlite3.connect(db_name)
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     # get results from customers
#     cur.execute("select * from customers")
#     rows = cur.fetchall()
#     conn.close()
#     return render_template('customers.html', rows=rows)

# @app.route('/customer_details/<id>')
# def customer_details(id):
#     conn = sqlite3.connect(db_name)
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     # get results from customers
#     cur.execute("select * from customers WHERE id=?", (id,))# do not forget the comma which makes the parameter a tuple
#     customer = cur.fetchall()
#     # get results from orders for this customer id
#     cur.execute("select * from orders WHERE customer_id=?", (id,))
#     orders = cur.fetchall()

#     conn.close()
#     return render_template('customer_details.html', customer=customer, orders=orders)

# @app.route('/orders')
# def orders():
#     conn = sqlite3.connect(db_name)
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     # get results from orders
#     cur.execute("select * from orders")
#     rows = cur.fetchall()
#     conn.close()
#     return render_template('orders.html', rows=rows)

# @app.route('/order_details/<id>')
# def order_details(id):
#     conn = sqlite3.connect(db_name)
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     # get results from orders
#     cur.execute("select * from orders WHERE id=?", (id,))
#     order = cur.fetchall()

#     customer_id=order[0]["customer_id"]
#     # get results from customers for this order
#     cur.execute("select * from customers WHERE id=?", (customer_id,))
#     customer = cur.fetchall()

#     # get results from line_items
#     cur.execute("select * from line_items WHERE order_id=?", (id,))
#     items = cur.fetchall()

#     conn.close()
#     return render_template('order_details.html', order=order, customer=customer, items=items)

if __name__ == '__main__':
    app.run(debug=True)   