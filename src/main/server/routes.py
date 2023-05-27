from flask import request, jsonify, make_response
from src.main.server.server import app
from src.views.register_product_view import RegisterProductsViews
from src.views.search_products_view import SearchProductViews
from src.main.composer.register_product_composer import register_product_composer
from src.main.composer.search_composer import search_composer
from src.main.adapter.request_adapter import request_adapter

@app.route("/register_product", methods=["POST"])
def register_product_route():
    request_adapter = register_product_composer()
    http_response = request_adapter.register_products_view(request)
    
    response = make_response(jsonify(http_response["data"]), http_response["status_code"])
    return response

@app.route("/register_product/search_product", methods=["GET"])
def search_product_route():
    search_route = search_composer()
    http_response = search_route.search_product_view(request.args)
        
    print(f"http_response: {http_response}")
    return jsonify(http_response["data"]), http_response["status_code"]