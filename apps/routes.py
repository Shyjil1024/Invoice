from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from datetime import datetime
from bson.objectid import ObjectId
from . import mongo
from .forms import InvoiceForm

routes_bp = Blueprint('routes', __name__)

# Route to create invoice
@routes_bp.route('/create_invoice', methods=['GET', 'POST'])
def create_invoice():
    form = InvoiceForm()
    if form.validate_on_submit():
        products = []
        total_amount = 0

        for product in form.products.data:
            product_name = product.product_name.data
            quantity = product.quantity.data
            price = product.price.data
            total_amount += quantity * price
            products.append({
                "product_name": product_name,
                "quantity": quantity,
                "price": price
            })

        invoice = {
            "products": products,
            "total_amount": total_amount,
            "date": datetime.now()
        }

        mongo.db.invoices.insert_one(invoice)
        flash("Invoice created successfully!", "success")
        return redirect(url_for('routes.create_invoice'))

    initial_product_count = len(form.products.data) if form.products.data else 0
    return render_template('create_invoice.html', form=form, initial_product_count=initial_product_count)

# Route to fetch product suggestions for autocomplete
@routes_bp.route('/product_search', methods=['GET'])
def product_search():
    query = request.args.get('query', '')
    products = mongo.db.products.find({"product_name": {"$regex": query, "$options": "i"}})
    product_list = [{"product_name": product['product_name'], "price": product['price']} for product in products]
    return jsonify(product_list)

# Route to fetch product price when a product is selected
@routes_bp.route('/get_product_price', methods=['GET'])
def get_product_price():
    product_name = request.args.get('product_name', '')
    product = mongo.db.products.find_one({"product_name": product_name})
    if product:
        return jsonify({"price": product['price']})
    return jsonify({"price": 0})