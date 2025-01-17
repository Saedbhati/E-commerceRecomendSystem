from flask import Flask, render_template, make_response, request
from database import *
import json
app = Flask(__name__)   

@app.route('/')
def index():
    product_data = GetProduct()
    clicked_product = []
    home_recommend={}
    if request.cookies.get('clicked_product') is not None:
        clicked_product = json.loads(request.cookies.get('clicked_product'))
        home_recommend = homeRecommendation(clicked_product)
    res= make_response(render_template('index.html', data=product_data, clicked_product=clicked_product, home_recommend=home_recommend))
    if request.cookies.get('clicked_product') is None:
        res.set_cookie('clicked_product', '[]')
    return res

@app.route("/product/<id>")
def product(id):
    product_data = GetProductById(int(id))
    
    if product_data is None:
        return "Product not found", 404
    clicked_product = request.cookies.get('clicked_product')
    if clicked_product:
        clicked_product = json.loads(clicked_product)
    else:
        clicked_product = []

    if id not in clicked_product:
        clicked_product.append(id)
    recommend = vectorSearch(product_data['product_name'])
    res = make_response(render_template('product.html', id=id, data=product_data, recommend=recommend))
    
    # Update the cookie with the new clicked_product list
    res.set_cookie('clicked_product', json.dumps(clicked_product))
    
    return res
if __name__ == '__main__':
    app.run(debug=True)