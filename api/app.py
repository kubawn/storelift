from flask import Flask, request
import sqlalchemy as sa

app = Flask(__name__)
engine = sa.create_engine("mysql+pymysql://root:storelift@store_db:3306/store_db")

@app.route('/take', methods=['POST'])
def take_item():
    item = request.form["item"]
    user = request.form["id"]
    with engine.connect() as conn:
        res = conn.execute("SELECT * FROM users_inside WHERE ID = {}".format(user))
        if res.rowcount is not 1:
            return "user is not in store"
        res = conn.execute("SELECT * FROM item_prices WHERE Item_ID = {}".format(item))
        if res.rowcount is not 1:
            return "item is not in store"
        res = conn.execute("INSERT INTO items_in_carts VALUES ({}, {})".format(user, item))
    return "item in cart: user_id={}, item_id={}".format(user, item)

@app.route('/put', methods=['POST'])
def return_item():
    item = request.form["item"]
    user = request.form["id"]
    with engine.connect() as conn:
        res = conn.execute("DELETE FROM items_in_carts WHERE ID = {} and Item_ID = {} LIMIT 1".format(user, item))
    if res.rowcount is 0:
        return "item/user conbination not found in the cart"
    return "returned item: user_id={}, item_id={}".format(user, item)

@app.route('/enter', methods=['POST'])
def enter():
    user = request.form["id"]
    with engine.connect() as conn:
        res = conn.execute("INSERT INTO users_inside VALUES ({})".format(user))
    if res.rowcount is not 1:
        return "user with that ID doesn't exist or is already in the store"
    return "user {} entered the store".format(user)

@app.route('/leave', methods=['POST'])
def leave():
    user = request.form["id"]
    with engine.connect() as conn:
        res = conn.execute("SELECT * FROM users_inside WHERE ID = {}".format(user))
        if res.rowcount is not 1:
            return "user with that ID is not in the store"
        res = conn.execute("SELECT Item_ID FROM items_in_carts WHERE ID = {}".format(user))
        items = list(res)
        res = conn.execute("SELECT * FROM item_prices")
        item_prices = {a:b for (a,b) in list(res)}
        price = sum([item_prices[item[0]] for item in items])
        res = conn.execute("SELECT CREDITS FROM user_registry WHERE ID = {}".format(user))
        credit = list(res)[0][0]
        if price > credit:
            return "user can't leave - not enough money to pay for things in the cart"
        res = conn.execute("UPDATE user_registry SET CREDITS = {} WHERE ID = {}".format(credit - price, user))
        res = conn.execute("DELETE FROM items_in_carts WHERE ID = {}".format(user))
        res = conn.execute("DELETE FROM users_inside WHERE ID = {}".format(user))
    return "user {} left the store after paying: {}, credits left: {}".format(user, price, credit - price)

@app.route('/state', methods=['GET'])
def store_state():
    with engine.connect() as conn:
        res = conn.execute("SELECT * FROM users_inside")
        users = "Users inside: {}. ".format(str(list(res)))
        res = conn.execute("SELECT * FROM items_in_carts")
        items = "Items in carts: {}. ".format(str(list(res)))
        res = conn.execute("SELECT * FROM user_registry")
        registry = "Registered users and their credits: {}. ".format(str(list(res)))
        res = conn.execute("SELECT * FROM item_prices")
        item_registry = "Item price list: {}. ".format(str(list(res)))
        return users + "\n" + items + "\n" + registry + "\n" + item_registry

@app.route('/register_item', methods=['POST'])
def register_item():
    item = request.form["item"]
    price = request.form["price"]
    with engine.connect() as conn:
        res = conn.execute("INSERT INTO item_prices VALUES ({}, {})".format(item, price))
    if res.rowcount is not 1:
        return "item with that id already exists"
    return "registered item: id = {}, price = {}".format(item, price)

@app.route('/register_customer', methods=['POST'])
def register_customer():
    user = request.form["id"]
    credit = request.form["credits"]
    with engine.connect() as conn:
        res = conn.execute("INSERT INTO user_registry VALUES ({}, {})".format(user, credit))
    if res.rowcount is not 1:
        return "user with that id already exists"
    return "registered customer: {}, {}".format(user, credit)

@app.route('/')
def landing_page():
    return 'landing page'

if __name__ == "__main__":
    app.run(host='0.0.0.0')