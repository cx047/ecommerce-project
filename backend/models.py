from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(100), nullable=False, default='general')
    stock = db.Column(db.Integer, default=100)
    specifications = db.Column(db.Text, nullable=True)  # JSON string: [{"name":"颜色","options":["红","黑"]}]
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'category': self.category,
            'stock': self.stock,
            'specifications': json.loads(self.specifications) if self.specifications else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    selected_specs = db.Column(db.Text, nullable=True)  # JSON string: {"颜色":"红","尺寸":"M"}
    session_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref='cart_items')

    def to_dict(self):
        specs = json.loads(self.selected_specs) if self.selected_specs else {}
        spec_str = ', '.join([f"{k}: {v}" for k, v in specs.items()]) if specs else ''
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'selected_specs': specs,
            'spec_details': spec_str,
            'session_id': self.session_id,
            'product': self.product.to_dict() if self.product else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    customer_name = db.Column(db.String(100), nullable=True)
    customer_email = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Float, nullable=False)
    selected_specs = db.Column(db.Text, nullable=True)

    product = db.relationship('Product')

    def to_dict(self):
        specs = json.loads(self.selected_specs) if self.selected_specs else {}
        spec_str = ', '.join([f"{k}: {v}" for k, v in specs.items()]) if specs else ''
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price_at_time': self.price_at_time,
            'selected_specs': specs,
            'spec_details': spec_str,
            'product': self.product.to_dict() if self.product else None
        }