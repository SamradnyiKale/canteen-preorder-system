from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

cart = []
coupon_applied = False
discount = 0
token_counter = 100

menu = {
    "Sandwiches": {
        "Veg Sandwich": {"price": 50, "image": "veg sandwich.jpg"},
        "Grilled Sandwich": {"price": 70, "image": "grilled_sandwich.jpg"},
        "Paneer Sandwich": {"price": 90, "image": "paneer_sandwich.jpg"},
        "Aloo cheese Sandwich": {"price": 80, "image": "aloo_cheese_sandwich.jpg"},
    },

    "Burgers": {
        "Veg Burger": {"price": 60, "image": "veg_burger.jpg"},
        "Cheese Burger": {"price": 80, "image": "cheese burger.jpg"},
    },

    "Pizza": {
        "Margherita Pizza": {"price": 120, "image": "margherita.jpg"},
        "Farmhouse Pizza": {"price": 150, "image": "farmhouse.jpg"},
        "Veg Pizza": {"price": 140, "image": "veg_pizza.jpg"},
    },

    "Dosa": {
        "Plain Dosa": {"price": 40, "image": "plain_dosa.jpg"},
        "Masala Dosa": {"price": 70, "image": "masala_dosa.jpg"},
        "Cheese Dosa": {"price": 90, "image": "cheese_dosa.jpg"},
        "Rava Dosa": {"price": 50, "image": "rava_dosa.jpg"},
        "Medu Vada": {"price": 30, "image": "meduvada.jpg"},
    },

    "Snacks": {
        "Vada Pav": {"price": 20, "image": "vadapav.jpg"},
        "Samosa": {"price": 15, "image": "samosa.jpg"},
        "Omelette": {"price": 30, "image": "omelette.jpg"},
        "misal Pav": {"price": 50, "image": "misal_pav.jpg"},
        "Aloo paratha": {"price": 40, "image": "aloo_paratha.jpg"},
    },
    "Garlic Bread": {
        "Garlic Bread": {"price": 80, "image": "garlic_bread.jpg"},
        "Cheese Garlic Bread": {"price": 100, "image": "cheese_garlic_bread.jpg"},
    },          

    "Maggi": {
        "Plain Maggi": {"price": 40, "image": "plain_maggi.jpg"},
        "Cheese Maggi": {"price": 60, "image": "cheese_maggi.jpg"},
    },
    "Juices": {
        "Orange Juice": {"price": 50, "image": "orange_juice.jpg"},
        "Apple Juice": {"price": 50, "image": "apple_juice.jpg"},
        "Mango Juice": {"price": 60, "image": "mango_juice.jpg"},
    },
    "Pasta": {
        "White Pasta": {"price": 100, "image": "white_sauce.jpg"},
        "Red Pasta": {"price": 100, "image": "red_sauce.jpg"},
    },


}

@app.route("/")
def index():
    return render_template("index.html", menu=menu)

# ADD TO CART
@app.route("/add/<item>")
def add_to_cart(item):
    global token_counter   # 🔥 IMPORTANT LINE

    for category in menu:
        if item in menu[category]:
            price = menu[category][item]["price"]

            token_counter += 1   # now works ✅

            cart.append({
                "item": item,
                "price": price,
                "qty": 1,
                "status": "Pending",
                "token": token_counter,
                "instruction": ""
            })

    return redirect(url_for("index"))

# INCREASE QTY
@app.route("/inc/<item>")
def increase(item):
    for i in cart:
        if i["item"] == item:
            i["qty"] += 1
    return redirect(url_for("view_cart"))

# DECREASE QTY
@app.route("/dec/<item>")
def decrease(item):
    for i in cart:
        if i["item"] == item and i["qty"] > 1:
            i["qty"] -= 1
    return redirect(url_for("view_cart"))

# UPDATE STATUS
@app.route("/status/<item>")
def status(item):
    for i in cart:
        if i["item"] == item:
            i["status"] = "Completed"
    return redirect(url_for("view_cart"))

# ADD INSTRUCTION
@app.route("/instruction/<item>", methods=["POST"])
def instruction(item):
    text = request.form["instruction"]
    for i in cart:
        if i["item"] == item:
            i["instruction"] = text
    return redirect(url_for("view_cart"))


# CART PAGE
@app.route("/cart")
def view_cart():
    total = sum(i["price"] * i["qty"] for i in cart)
    final = total - discount if coupon_applied else total

    return render_template("cart.html", cart=cart, total=total, final=final, discount=discount)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)