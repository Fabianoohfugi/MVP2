from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    quantity = Column(Integer)
    price = Column(Float)

engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
CORS(app)
CORS(app, origins=["http://127.0.0.1:5000", "http://localhost:5000"], methods=["GET", "POST", "PUT", "DELETE"])



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_products():
    products = session.query(Product).all()
    return jsonify({'success': True, 'products': [{'id': product.id, 'name': product.name, 'quantity': product.quantity, 'price': product.price} for product in products]})

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = session.query(Product).filter_by(id=product_id).first()
    if product:
        return jsonify({'success': True, 'product': {'id': product.id, 'name': product.name, 'quantity': product.quantity, 'price': product.price}})
    else:
        return jsonify({'success': False, 'error': 'Product not found'})

@app.route('/api/products', methods=['POST'])
def add_product():
    name = request.json['name']
    quantity = request.json['quantity']
    price = request.json['price']

    new_product = Product(name=name, quantity=quantity, price=price)
    session.add(new_product)
    session.commit()

    return jsonify({'success': True, 'product': {'id': new_product.id, 'name': new_product.name, 'quantity': new_product.quantity, 'price': new_product.price}})

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = session.query(Product).filter_by(id=product_id).first()
    if product:
        product.name = request.json['name']
        product.quantity = request.json['quantity']
        product.price = request.json['price']
        session.commit()
        return jsonify({'success': True, 'product': {'id': product.id, 'name': product.name, 'quantity': product.quantity, 'price': product.price}})
    else:
        return jsonify({'success': False, 'error': 'Product not found'})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = session.query(Product).filter_by(id=product_id).first()
    print("Product found:", product)
    if product:
        session.delete(product)
        session.commit()
        print("Product deleted:", product)
        return jsonify({'success': True}), 204
    else:
        print("Product not found")
        return jsonify({'success': False, 'error': 'Product not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)