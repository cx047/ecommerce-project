from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, Product, CartItem, Order, OrderItem
from seed_data import seed_database
import uuid

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS for all routes
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Session-ID"]
        }
    })
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        seed_database()
    
    # ========== Helper Functions ==========
    def get_session_id():
        """Get or create session ID from request headers"""
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            session_id = str(uuid.uuid4())
        return session_id
    
    # ========== Product Routes ==========
    @app.route('/api/products', methods=['GET'])
    def get_products():
        """Get all products with optional filtering by category"""
        category = request.args.get('category')
        search = request.args.get('search')
        
        query = Product.query
        
        if category:
            query = query.filter_by(category=category)
        
        if search:
            query = query.filter(Product.name.contains(search))
        
        products = query.all()
        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in products],
            'count': len(products)
        })
    
    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        """Get a single product by ID"""
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'success': True,
            'data': product.to_dict()
        })
    
    @app.route('/api/products/categories', methods=['GET'])
    def get_categories():
        """Get all unique product categories"""
        categories = db.session.query(Product.category).distinct().all()
        return jsonify({
            'success': True,
            'data': [c[0] for c in categories]
        })
    
    # ========== Cart Routes ==========
    @app.route('/api/cart', methods=['GET'])
    def get_cart():
        """Get all items in the cart for current session"""
        session_id = get_session_id()
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
        
        total = sum(item.product.price * item.quantity for item in cart_items if item.product)
        
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in cart_items],
            'total': round(total, 2),
            'count': len(cart_items),
            'session_id': session_id
        })
    
    @app.route('/api/cart', methods=['POST'])
    def add_to_cart():
        """Add a product to cart"""
        data = request.get_json()
        session_id = get_session_id()
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id:
            return jsonify({'success': False, 'error': 'Product ID is required'}), 400
        
        product = Product.query.get_or_404(product_id)
        
        if product.stock < quantity:
            return jsonify({
                'success': False, 
                'error': f'Not enough stock. Available: {product.stock}'
            }), 400
        
        # Check if item already in cart
        cart_item = CartItem.query.filter_by(
            session_id=session_id, 
            product_id=product_id
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                product_id=product_id,
                quantity=quantity,
                session_id=session_id
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': cart_item.to_dict(),
            'message': 'Item added to cart'
        })
    
    @app.route('/api/cart/<int:item_id>', methods=['PUT'])
    def update_cart_item(item_id):
        """Update cart item quantity"""
        data = request.get_json()
        session_id = get_session_id()
        
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            session_id=session_id
        ).first_or_404()
        
        quantity = data.get('quantity', 1)
        
        if quantity <= 0:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Item removed from cart'
            })
        
        if cart_item.product and cart_item.product.stock < quantity:
            return jsonify({
                'success': False,
                'error': f'Not enough stock. Available: {cart_item.product.stock}'
            }), 400
        
        cart_item.quantity = quantity
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': cart_item.to_dict(),
            'message': 'Cart updated'
        })
    
    @app.route('/api/cart/<int:item_id>', methods=['DELETE'])
    def remove_from_cart(item_id):
        """Remove item from cart"""
        session_id = get_session_id()
        
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            session_id=session_id
        ).first_or_404()
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item removed from cart'
        })
    
    @app.route('/api/cart/clear', methods=['DELETE'])
    def clear_cart():
        """Clear all items from cart"""
        session_id = get_session_id()
        CartItem.query.filter_by(session_id=session_id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cart cleared'
        })
    
    # ========== Order Routes ==========
    @app.route('/api/orders', methods=['GET'])
    def get_orders():
        """Get all orders for current session"""
        session_id = get_session_id()
        orders = Order.query.filter_by(session_id=session_id).order_by(
            Order.created_at.desc()
        ).all()
        
        return jsonify({
            'success': True,
            'data': [order.to_dict() for order in orders],
            'count': len(orders)
        })
    
    @app.route('/api/orders', methods=['POST'])
    def create_order():
        """Create a new order from cart items"""
        data = request.get_json()
        session_id = get_session_id()
        
        # Get all cart items
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
        
        if not cart_items:
            return jsonify({
                'success': False,
                'error': 'Cart is empty'
            }), 400
        
        # Calculate total
        total_amount = sum(
            item.product.price * item.quantity 
            for item in cart_items 
            if item.product
        )
        
        # Create order
        order = Order(
            session_id=session_id,
            total_amount=total_amount,
            customer_name=data.get('customer_name'),
            customer_email=data.get('customer_email'),
            status='completed'
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items and update stock
        for cart_item in cart_items:
            if cart_item.product:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price_at_time=cart_item.product.price
                )
                db.session.add(order_item)
                
                # Update product stock
                cart_item.product.stock -= cart_item.quantity
        
        # Clear cart
        CartItem.query.filter_by(session_id=session_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': order.to_dict(),
            'message': 'Order created successfully'
        })
    
    @app.route('/api/orders/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        """Get a single order by ID"""
        session_id = get_session_id()
        order = Order.query.filter_by(
            id=order_id, 
            session_id=session_id
        ).first_or_404()
        
        return jsonify({
            'success': True,
            'data': order.to_dict()
        })
    
    # ========== Health Check ==========
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """API health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'ecommerce-api',
            'version': '1.0.0'
        })
    
    # ========== Error Handlers ==========
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app

# Create application instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
