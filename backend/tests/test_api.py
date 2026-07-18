"""
ecommerce API 单元测试

运行方式：
    cd backend
    python -m pytest tests/ -v

覆盖端点：
    - GET  /api/health
    - GET  /api/products
    - GET  /api/products/<id>
    - GET  /api/products/categories
    - POST /api/cart
    - GET  /api/cart
    - PUT  /api/cart/<id>
    - DELETE /api/cart/<id>
    - DELETE /api/cart/clear
    - POST /api/orders
    - GET  /api/orders
    - GET  /api/orders/<id>
"""

import pytest
import json
import sys
import os

# 确保可以导入 backend 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from config import Config
from models import db as _db, Product, CartItem, Order, OrderItem


class TestConfig(Config):
    """测试专用配置，使用内存 SQLite 数据库"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# ======================== Fixtures ========================

@pytest.fixture
def app():
    """创建测试用 Flask 应用，使用内存 SQLite 数据库"""
    application = create_app(TestConfig)

    with application.app_context():
        _db.create_all()
        from seed_data import seed_database
        seed_database()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def session_headers():
    """统一的测试会话 Header"""
    return {'X-Session-ID': 'test-session-123'}


@pytest.fixture
def another_session_headers():
    """另一个测试会话 Header，用于隔离测试"""
    return {'X-Session-ID': 'test-session-456'}


# ======================== Health 端点 ========================

class TestHealthEndpoint:
    """GET /api/health"""

    def test_health_check_returns_200(self, client):
        """健康检查端点应返回 200 状态码"""
        resp = client.get('/api/health')
        assert resp.status_code == 200

    def test_health_check_returns_correct_payload(self, client):
        """健康检查响应体应包含 status、service、version 字段"""
        resp = client.get('/api/health')
        data = resp.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'ecommerce-api'
        assert 'version' in data


# ======================== Products 端点 ========================

class TestGetProducts:
    """GET /api/products"""

    def test_get_products_returns_200(self, client):
        """获取商品列表应返回 200"""
        resp = client.get('/api/products')
        assert resp.status_code == 200

    def test_get_products_returns_success_true(self, client):
        """商品列表响应 success 应为 True"""
        resp = client.get('/api/products')
        data = resp.get_json()
        assert data['success'] is True

    def test_get_products_returns_data_list(self, client):
        """商品列表 data 应为列表"""
        resp = client.get('/api/products')
        data = resp.get_json()
        assert isinstance(data['data'], list)
        assert data['count'] > 0

    def test_get_products_count_matches_data_length(self, client):
        """count 字段应与 data 列表长度一致"""
        resp = client.get('/api/products')
        data = resp.get_json()
        assert data['count'] == len(data['data'])

    def test_get_products_filter_by_category(self, client):
        """按分类筛选应只返回该分类的商品"""
        resp = client.get('/api/products?category=electronics')
        data = resp.get_json()
        assert data['success'] is True
        for product in data['data']:
            assert product['category'] == 'electronics'

    def test_get_products_filter_by_category_empty_result(self, client):
        """使用不存在的分类筛选应返回空列表"""
        resp = client.get('/api/products?category=nonexistent')
        data = resp.get_json()
        assert data['success'] is True
        assert data['count'] == 0
        assert data['data'] == []

    def test_get_products_search_by_name(self, client):
        """按关键字搜索应返回名称包含关键字的商品"""
        resp = client.get('/api/products?search=耳机')
        data = resp.get_json()
        assert data['success'] is True
        assert data['count'] > 0
        for product in data['data']:
            assert '耳机' in product['name']

    def test_get_products_search_no_results(self, client):
        """搜索不存在的关键字应返回空列表"""
        resp = client.get('/api/products?search=xyz不存在的商品abc')
        data = resp.get_json()
        assert data['success'] is True
        assert data['count'] == 0

    def test_get_products_combined_category_and_search(self, client):
        """同时使用分类和搜索筛选"""
        resp = client.get('/api/products?category=electronics&search=键盘')
        data = resp.get_json()
        assert data['success'] is True
        for product in data['data']:
            assert product['category'] == 'electronics'
            assert '键盘' in product['name']


class TestGetProductDetail:
    """GET /api/products/<id>"""

    def test_get_product_by_id_returns_200(self, client):
        """获取存在的商品应返回 200"""
        resp = client.get('/api/products/1')
        assert resp.status_code == 200

    def test_get_product_by_id_returns_correct_product(self, client):
        """返回的商品 ID 应与请求一致"""
        resp = client.get('/api/products/1')
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['id'] == 1
        assert 'name' in data['data']
        assert 'price' in data['data']
        assert 'stock' in data['data']
        assert 'specifications' in data['data']

    def test_get_product_by_id_nonexistent_returns_404(self, client):
        """获取不存在的商品应返回 404"""
        resp = client.get('/api/products/99999')
        assert resp.status_code == 404


class TestGetCategories:
    """GET /api/products/categories"""

    def test_get_categories_returns_200(self, client):
        """获取分类列表应返回 200"""
        resp = client.get('/api/products/categories')
        assert resp.status_code == 200

    def test_get_categories_returns_list(self, client):
        """分类列表应为字符串列表"""
        resp = client.get('/api/products/categories')
        data = resp.get_json()
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert len(data['data']) > 0
        assert 'electronics' in data['data']

    def test_get_categories_are_unique(self, client):
        """分类列表不应有重复项"""
        resp = client.get('/api/products/categories')
        data = resp.get_json()
        assert len(data['data']) == len(set(data['data']))


# ======================== Cart 端点 ========================

class TestAddToCart:
    """POST /api/cart"""

    def test_add_to_cart_returns_201_like_success(self, client, session_headers):
        """添加商品到购物车应成功（实际返回 200）"""
        resp = client.post('/api/cart',
                            headers=session_headers,
                            json={'product_id': 1, 'quantity': 2})
        assert resp.status_code == 200

    def test_add_to_cart_returns_success(self, client, session_headers):
        """添加商品到购物车响应 success 应为 True"""
        resp = client.post('/api/cart',
                            headers=session_headers,
                            json={'product_id': 1, 'quantity': 1})
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['product_id'] == 1
        assert data['data']['quantity'] == 1

    def test_add_to_cart_with_specs(self, client, session_headers):
        """带规格参数添加商品到购物车"""
        specs = {'颜色': '曜石黑', '版本': '降噪版'}
        resp = client.post('/api/cart',
                            headers=session_headers,
                            json={
                                'product_id': 1,
                                'quantity': 1,
                                'selected_specs': specs
                            })
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['selected_specs'] == specs

    def test_add_to_cart_missing_product_id_returns_400(self, client, session_headers):
        """缺少 product_id 应返回 400"""
        resp = client.post('/api/cart',
                            headers=session_headers,
                            json={'quantity': 1})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data['success'] is False
        assert 'Product ID is required' in data['error']

    def test_add_to_cart_duplicate_item_increases_quantity(self, client, session_headers):
        """重复添加同商品（同规格）应增加数量而非新建记录"""
        # 第一次添加
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 1})
        # 第二次添加相同商品（无规格）
        resp = client.post('/api/cart',
                            headers=session_headers,
                            json={'product_id': 1, 'quantity': 2})
        data = resp.get_json()
        assert data['success'] is True
        # 同一商品同规格应合并，数量应为 1+2=3
        assert data['data']['quantity'] == 3

    def test_add_to_cart_exceeds_stock_returns_400(self, client, session_headers):
        """添加数量超过库存应返回 400"""
        # 使用 seed 数据中库存为 20 的商品（ID=5，意式浓缩咖啡机）
        resp = client.post('/api/cart',
                            headers=session_headers,
                            json={'product_id': 5, 'quantity': 999})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data['success'] is False
        assert 'Not enough stock' in data['error']

    def test_add_to_cart_nonexistent_product_returns_404(self, client, session_headers):
        """添加不存在的商品应返回 404"""
        resp = client.post('/api/cart',
                            headers=session_headers,
                            json={'product_id': 99999, 'quantity': 1})
        assert resp.status_code == 404


class TestGetCart:
    """GET /api/cart"""

    def test_get_empty_cart_returns_200(self, client, session_headers):
        """获取空购物车应返回 200，data 为空列表"""
        resp = client.get('/api/cart', headers=session_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data'] == []
        assert data['count'] == 0
        assert data['total'] == 0

    def test_get_cart_after_adding_item(self, client, session_headers):
        """添加商品后获取购物车应包含该商品"""
        # 先添加
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 2})
        # 再获取
        resp = client.get('/api/cart', headers=session_headers)
        data = resp.get_json()
        assert data['count'] == 1
        assert data['total'] > 0
        assert data['data'][0]['product_id'] == 1
        assert data['data'][0]['quantity'] == 2

    def test_get_cart_session_isolation(self, client, session_headers, another_session_headers):
        """不同 session 的购物车应完全隔离"""
        # Session A 添加商品
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 1})
        # Session B 的购物车应为空
        resp = client.get('/api/cart', headers=another_session_headers)
        data = resp.get_json()
        assert data['count'] == 0

    def test_get_cart_total_is_correct(self, client, session_headers, app):
        """购物车总价应为各商品 价格*数量 之和"""
        # 添加两个商品
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 2})  # 耳机 299 * 2
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 2, 'quantity': 1})  # 手表 599 * 1

        resp = client.get('/api/cart', headers=session_headers)
        data = resp.get_json()
        expected_total = 299.00 * 2 + 599.00 * 1
        assert data['total'] == expected_total


class TestUpdateCartItem:
    """PUT /api/cart/<id>"""

    def test_update_cart_item_quantity(self, client, session_headers):
        """更新购物车商品数量应成功"""
        # 先添加
        add_resp = client.post('/api/cart',
                                headers=session_headers,
                                json={'product_id': 1, 'quantity': 1})
        item_id = add_resp.get_json()['data']['id']

        # 更新数量为 5
        resp = client.put(f'/api/cart/{item_id}',
                           headers=session_headers,
                           json={'quantity': 5})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['quantity'] == 5

    def test_update_cart_item_quantity_zero_removes_item(self, client, session_headers):
        """将数量更新为 0 应删除该商品"""
        add_resp = client.post('/api/cart',
                                headers=session_headers,
                                json={'product_id': 1, 'quantity': 3})
        item_id = add_resp.get_json()['data']['id']

        resp = client.put(f'/api/cart/{item_id}',
                           headers=session_headers,
                           json={'quantity': 0})
        data = resp.get_json()
        assert data['success'] is True
        assert 'Item removed from cart' in data['message']

        # 确认购物车为空
        cart_resp = client.get('/api/cart', headers=session_headers)
        assert cart_resp.get_json()['count'] == 0

    def test_update_cart_item_exceeds_stock(self, client, session_headers):
        """更新数量超过库存应返回 400"""
        add_resp = client.post('/api/cart',
                                headers=session_headers,
                                json={'product_id': 1, 'quantity': 1})
        item_id = add_resp.get_json()['data']['id']

        # 耳机库存为 50，尝试更新为 999
        resp = client.put(f'/api/cart/{item_id}',
                           headers=session_headers,
                           json={'quantity': 999})
        assert resp.status_code == 400
        assert 'Not enough stock' in resp.get_json()['error']

    def test_update_cart_item_wrong_session_returns_404(self, client, session_headers, another_session_headers):
        """更新属于其他 session 的购物车项应返回 404"""
        # Session A 添加商品
        add_resp = client.post('/api/cart',
                                headers=session_headers,
                                json={'product_id': 1, 'quantity': 1})
        item_id = add_resp.get_json()['data']['id']

        # Session B 尝试更新
        resp = client.put(f'/api/cart/{item_id}',
                           headers=another_session_headers,
                           json={'quantity': 5})
        assert resp.status_code == 404


class TestRemoveCartItem:
    """DELETE /api/cart/<id>"""

    def test_remove_cart_item_returns_200(self, client, session_headers):
        """删除购物车商品应成功"""
        add_resp = client.post('/api/cart',
                                headers=session_headers,
                                json={'product_id': 1, 'quantity': 1})
        item_id = add_resp.get_json()['data']['id']

        resp = client.delete(f'/api/cart/{item_id}', headers=session_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert 'Item removed from cart' in data['message']

    def test_remove_cart_item_deletes_from_cart(self, client, session_headers):
        """删除后购物车不应再包含该商品"""
        add_resp = client.post('/api/cart',
                                headers=session_headers,
                                json={'product_id': 1, 'quantity': 1})
        item_id = add_resp.get_json()['data']['id']

        client.delete(f'/api/cart/{item_id}', headers=session_headers)

        cart_resp = client.get('/api/cart', headers=session_headers)
        assert cart_resp.get_json()['count'] == 0

    def test_remove_nonexistent_cart_item_returns_404(self, client, session_headers):
        """删除不存在的购物车商品应返回 404"""
        resp = client.delete('/api/cart/99999', headers=session_headers)
        assert resp.status_code == 404


class TestClearCart:
    """DELETE /api/cart/clear"""

    def test_clear_cart_returns_200(self, client, session_headers):
        """清空购物车应返回 200"""
        # 先添加商品
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 1})

        resp = client.delete('/api/cart/clear', headers=session_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert 'Cart cleared' in data['message']

    def test_clear_cart_empties_all_items(self, client, session_headers):
        """清空后购物车应完全为空"""
        # 添加多个商品
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 1})
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 2, 'quantity': 1})

        client.delete('/api/cart/clear', headers=session_headers)

        cart_resp = client.get('/api/cart', headers=session_headers)
        data = cart_resp.get_json()
        assert data['count'] == 0
        assert data['total'] == 0

    def test_clear_empty_cart_still_succeeds(self, client, session_headers):
        """清空一个已经是空的购物车也应成功"""
        resp = client.delete('/api/cart/clear', headers=session_headers)
        assert resp.status_code == 200


# ======================== Orders 端点 ========================

class TestCreateOrder:
    """POST /api/orders"""

    def test_create_order_from_cart(self, client, session_headers):
        """从购物车创建订单应成功"""
        # 先添加商品到购物车
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 2})

        # 创建订单
        resp = client.post('/api/orders',
                            headers=session_headers,
                            json={
                                'customer_name': '测试用户',
                                'customer_email': 'test@example.com'
                            })
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['status'] == 'completed'
        assert data['data']['customer_name'] == '测试用户'
        assert data['data']['customer_email'] == 'test@example.com'
        assert data['data']['total_amount'] > 0

    def test_create_order_clears_cart(self, client, session_headers):
        """创建订单后购物车应被清空"""
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 1})

        client.post('/api/orders',
                     headers=session_headers,
                     json={'customer_name': '用户', 'customer_email': 'a@b.com'})

        cart_resp = client.get('/api/cart', headers=session_headers)
        assert cart_resp.get_json()['count'] == 0

    def test_create_order_deducts_stock(self, client, session_headers, app):
        """创建订单后商品库存应相应减少"""
        # 获取商品初始库存
        with app.app_context():
            product = Product.query.get(1)
            initial_stock = product.stock

        # 添加 3 件到购物车并下单
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 3})
        client.post('/api/orders',
                     headers=session_headers,
                     json={'customer_name': '用户', 'customer_email': 'a@b.com'})

        with app.app_context():
            product = Product.query.get(1)
            assert product.stock == initial_stock - 3

    def test_create_order_empty_cart_returns_400(self, client, session_headers):
        """购物车为空时创建订单应返回 400"""
        resp = client.post('/api/orders',
                            headers=session_headers,
                            json={'customer_name': '用户', 'customer_email': 'a@b.com'})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data['success'] is False
        assert 'Cart is empty' in data['error']

    def test_create_order_without_customer_info(self, client, session_headers):
        """不传客户信息创建订单也应成功（字段可选）"""
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 1})

        resp = client.post('/api/orders',
                            headers=session_headers,
                            json={})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True

    def test_create_order_with_multiple_items(self, client, session_headers):
        """创建包含多个商品的订单"""
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 1})
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 2, 'quantity': 2})

        resp = client.post('/api/orders',
                            headers=session_headers,
                            json={
                                'customer_name': '多商品测试',
                                'customer_email': 'multi@test.com'
                            })
        data = resp.get_json()
        assert data['success'] is True
        assert len(data['data']['items']) >= 2


class TestGetOrders:
    """GET /api/orders"""

    def test_get_orders_empty_returns_200(self, client, session_headers):
        """无订单时获取订单列表应返回 200，data 为空列表"""
        resp = client.get('/api/orders', headers=session_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data'] == []
        assert data['count'] == 0

    def test_get_orders_returns_created_order(self, client, session_headers):
        """创建订单后应能在订单列表中查到"""
        # 添加商品并创建订单
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 1})
        client.post('/api/orders',
                     headers=session_headers,
                     json={'customer_name': '用户', 'customer_email': 'a@b.com'})

        resp = client.get('/api/orders', headers=session_headers)
        data = resp.get_json()
        assert data['count'] == 1
        assert data['data'][0]['customer_name'] == '用户'

    def test_get_orders_session_isolation(self, client, session_headers, another_session_headers):
        """不同 session 的订单应隔离"""
        # Session A 创建订单
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 1})
        client.post('/api/orders',
                     headers=session_headers,
                     json={'customer_name': 'A', 'customer_email': 'a@b.com'})

        # Session B 不应有订单
        resp = client.get('/api/orders', headers=another_session_headers)
        assert resp.get_json()['count'] == 0

    def test_get_orders_returns_newest_first(self, client, session_headers):
        """订单列表应按创建时间倒序排列"""
        # 创建多个订单
        for i in range(3):
            client.post('/api/cart',
                         headers=session_headers,
                         json={'product_id': 1, 'quantity': 1})
            client.post('/api/orders',
                         headers=session_headers,
                         json={'customer_name': f'用户{i}', 'customer_email': f'{i}@b.com'})

        resp = client.get('/api/orders', headers=session_headers)
        data = resp.get_json()
        assert data['count'] == 3
        # 第一个应是最新的
        assert data['data'][0]['customer_name'] == '用户2'


class TestGetOrderDetail:
    """GET /api/orders/<id>"""

    def test_get_order_by_id_returns_200(self, client, session_headers):
        """获取存在的订单应返回 200"""
        # 创建订单
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 1})
        order_resp = client.post('/api/orders',
                                  headers=session_headers,
                                  json={'customer_name': '用户', 'customer_email': 'a@b.com'})
        order_id = order_resp.get_json()['data']['id']

        resp = client.get(f'/api/orders/{order_id}', headers=session_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['id'] == order_id
        assert 'items' in data['data']

    def test_get_order_detail_contains_items(self, client, session_headers):
        """订单详情应包含订单明细列表"""
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 2})
        order_resp = client.post('/api/orders',
                                  headers=session_headers,
                                  json={'customer_name': '用户', 'customer_email': 'a@b.com'})
        order_id = order_resp.get_json()['data']['id']

        resp = client.get(f'/api/orders/{order_id}', headers=session_headers)
        data = resp.get_json()
        items = data['data']['items']
        assert len(items) == 1
        assert items[0]['quantity'] == 2
        assert 'price_at_time' in items[0]
        assert items[0]['product'] is not None

    def test_get_order_wrong_session_returns_404(self, client, session_headers, another_session_headers):
        """获取属于其他 session 的订单应返回 404"""
        client.post('/api/cart',
                     headers=session_headers,
                     json={'product_id': 1, 'quantity': 1})
        order_resp = client.post('/api/orders',
                                  headers=session_headers,
                                  json={'customer_name': 'A', 'customer_email': 'a@b.com'})
        order_id = order_resp.get_json()['data']['id']

        resp = client.get(f'/api/orders/{order_id}', headers=another_session_headers)
        assert resp.status_code == 404

    def test_get_nonexistent_order_returns_404(self, client, session_headers):
        """获取不存在的订单应返回 404"""
        resp = client.get('/api/orders/99999', headers=session_headers)
        assert resp.status_code == 404
