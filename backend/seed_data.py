from models import db, Product
import json

def seed_database():
    """Seed the database with sample products. Always refresh to ensure data consistency."""
    # Clear existing products and related cart/order items
    from models import CartItem, Order, OrderItem
    OrderItem.query.delete()
    Order.query.delete()
    CartItem.query.delete()
    Product.query.delete()
    db.session.commit()

    sample_products = [
        {
            'name': '无线蓝牙耳机 Pro',
            'description': '高音质降噪无线蓝牙耳机，支持主动降噪，续航30小时，IPX7防水等级。采用最新蓝牙5.3技术，连接稳定低延迟。',
            'price': 299.00,
            'image_url': '',
            'category': 'electronics',
            'stock': 50,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['曜石黑', '象牙白', '天空蓝']},
                {'name': '版本', 'options': ['标准版', '降噪版']}
            ])
        },
        {
            'name': '智能运动手表',
            'description': '多功能智能手表，支持心率监测、血氧检测、GPS定位。50米防水，7天超长续航，100+运动模式。',
            'price': 599.00,
            'image_url': '',
            'category': 'electronics',
            'stock': 30,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['深空灰', '星光银', '玫瑰金']},
                {'name': '表带', 'options': ['硅胶', '金属', '真皮']}
            ])
        },
        {
            'name': '极简纯棉T恤',
            'description': '100%新疆长绒棉，亲肤透气。经典版型设计，多色可选。经过预缩水处理，不易变形。',
            'price': 89.00,
            'image_url': '',
            'category': 'clothing',
            'stock': 200,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['白色', '黑色', '灰色', '藏青']},
                {'name': '尺码', 'options': ['S', 'M', 'L', 'XL', 'XXL']}
            ])
        },
        {
            'name': '复古牛仔外套',
            'description': '经典复古水洗牛仔外套，宽松版型。采用优质丹宁面料，耐磨耐穿。百搭款式，四季皆宜。',
            'price': 259.00,
            'image_url': '',
            'category': 'clothing',
            'stock': 80,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['浅蓝', '深蓝', '黑色']},
                {'name': '尺码', 'options': ['S', 'M', 'L', 'XL']}
            ])
        },
        {
            'name': '意式浓缩咖啡机',
            'description': '家用半自动咖啡机，15Bar高压萃取。蒸汽奶泡系统，可制作拿铁、卡布奇诺等。不锈钢机身，易于清洁。',
            'price': 899.00,
            'image_url': '',
            'category': 'home',
            'stock': 20,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['经典银', '复古红']},
                {'name': '功率', 'options': ['850W', '1050W']}
            ])
        },
        {
            'name': '北欧风台灯',
            'description': '简约北欧设计LED台灯，三档色温可调，无极亮度调节。护眼无频闪，USB充电接口。适合卧室、书房使用。',
            'price': 159.00,
            'image_url': '',
            'category': 'home',
            'stock': 60,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['白色', '原木色', '深灰']},
                {'name': '光源', 'options': ['暖光', '白光', '三色变光']}
            ])
        },
        {
            'name': '机械键盘 RGB',
            'description': '87键机械键盘，青轴/红轴可选。全键无冲，RGB背光支持自定义灯效。PBT键帽，手感舒适持久耐用。',
            'price': 399.00,
            'image_url': '',
            'category': 'electronics',
            'stock': 40,
            'specifications': json.dumps([
                {'name': '轴体', 'options': ['青轴', '红轴', '茶轴']},
                {'name': '配色', 'options': ['黑白', '粉白', '灰白']}
            ])
        },
        {
            'name': '便携双肩背包',
            'description': '商务休闲两用双肩包，防水面料。多隔层设计，可容纳15.6英寸笔记本。人体工学背负系统，减轻肩部压力。',
            'price': 199.00,
            'image_url': '',
            'category': 'clothing',
            'stock': 100,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['黑色', '灰色', '军绿']},
                {'name': '容量', 'options': ['20L', '25L']}
            ])
        },
        {
            'name': '香薰蜡烛套装',
            'description': '天然大豆蜡香薰蜡烛，3种香型组合。燃烧时间约40小时/罐。无铅棉芯，燃烧干净无黑烟。',
            'price': 129.00,
            'image_url': '',
            'category': 'home',
            'stock': 70,
            'specifications': json.dumps([
                {'name': '香型', 'options': ['薰衣草', '柑橘', '檀香']},
                {'name': '规格', 'options': ['单罐', '三罐套装']}
            ])
        },
        {
            'name': '无线充电器',
            'description': '15W快充无线充电器，支持多种设备。智能温控，异物检测。简约设计，即放即充。',
            'price': 79.00,
            'image_url': '',
            'category': 'electronics',
            'stock': 150,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['白色', '黑色']},
                {'name': '功率', 'options': ['10W', '15W']}
            ])
        }
    ]

    for product_data in sample_products:
        product = Product(**product_data)
        db.session.add(product)

    db.session.commit()
    print(f"Seeded {len(sample_products)} products to database")
