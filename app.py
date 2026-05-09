from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Menu table
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# Orders table
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)

# Reservation table
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    table_number = db.Column(db.Integer, nullable=False)

# Home page
@app.route('/')
def home():

    menu_items = Menu.query.all()

    return render_template(
        'index.html',
        menu_items=menu_items
    )

# Order page
@app.route('/order/<int:item_id>', methods=['GET', 'POST'])
def order(item_id):

    item = Menu.query.get_or_404(item_id)

    if request.method == 'POST':

        customer_name = request.form['customer_name']

        new_order = Order(
            customer_name=customer_name,
            item_name=item.item_name
        )

        # Reduce stock
        if item.stock > 0:
            item.stock -= 1

        db.session.add(new_order)
        db.session.commit()

        return f"Order placed successfully for {item.item_name}!"

    return render_template(
        'order.html',
        item=item
    )

# Reservation page
@app.route('/reserve', methods=['GET', 'POST'])
def reserve():

    if request.method == 'POST':

        customer_name = request.form['customer_name']
        table_number = request.form['table_number']

        reservation = Reservation(
            customer_name=customer_name,
            table_number=table_number
        )

        db.session.add(reservation)
        db.session.commit()

        return "Table Reserved Successfully!"

    return render_template('reserve.html')

# Add sample menu
@app.route('/add')
def add():

    if Menu.query.count() == 0:

        item1 = Menu(
            item_name='Pizza',
            price=299,
            stock=10
        )

        item2 = Menu(
            item_name='Burger',
            price=199,
            stock=15
        )

        item3 = Menu(
            item_name='Pasta',
            price=249,
            stock=12
        )

        item4 = Menu(
            item_name='French Fries',
            price=149,
            stock=20
        )

        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.add(item4)

        db.session.commit()

    return "Menu Added Successfully!"

# Create database
with app.app_context():
    db.create_all()

# Run app
if __name__ == '__main__':
    app.run(debug=True)