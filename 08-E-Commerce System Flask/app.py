from flask import Flask, render_template, request, redirect, session
from database import get_db
import models

app = Flask(__name__)
app.secret_key = "yoursecretkey"

@app.route("/")
def home():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template("index.html", products=products)

@app.route("/product/<int:id>")
def product_page(id):
    db = get_db()
    product = db.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
    return render_template("product.html", product=product)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    cart = session.get("cart", [])
    cart.append(id)
    session["cart"] = cart
    return redirect("/cart")

@app.route("/cart")
def cart():
    cart_ids = session.get("cart", [])
    db = get_db()

    items = []
    total = 0

    for product_id in cart_ids:
        product = db.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
        items.append(product)
        total += product["price"]

    return render_template("cart.html", items=items, total=total)

@app.route("/remove/<int:id>")
def remove_item(id):
    cart = session.get("cart", [])
    if id in cart:
        cart.remove(id)
    session["cart"] = cart
    return redirect("/cart")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_db()
        email = request.form["email"]
        password = request.form["password"]

        user = db.execute("SELECT * FROM users WHERE email=? AND password=?", 
                          (email, password)).fetchone()

        if user:
            session["user"] = user["id"]
            return redirect("/")
        else:
            return "Invalid login"

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                   (request.form["name"], request.form["email"], request.form["password"]))
        db.commit()
        return redirect("/login")
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
