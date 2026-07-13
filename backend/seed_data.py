from models import db, Product

def seed_database():
    """Seed the database with sample products if empty"""
    if Product.query.first():
        return  # Database already has data
    
    sample_products = [
        {
            'name': '无线蓝牙耳机 Pro',
            'description': '高音质降噪无线蓝牙耳机，支持主动降噪，续航30小时，IPX7防水等级。采用最新蓝牙5.3技术，连接稳定低延迟。',
            'price': 299.00,
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',
            'category': 'electronics',
            'stock': 50
        },
        {
            'name': '智能运动手表',
            'description': '多功能智能手表，支持心率监测、血氧检测、GPS定位。50米防水，7天超长续航，100+运动模式。',
            'price': 599.00,
            'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop',
            'category': 'electronics',
            'stock': 30
        },
        {
            'name': '极简纯棉T恤',
            'description': '100%新疆长绒棉，亲肤透气。经典版型设计，多色可选。经过预缩水处理，不易变形。',
            'price': 89.00,
            'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop',
            'category': 'clothing',
            'stock': 200
        },
        {
            'name': '复古牛仔外套',
            'description': '经典复古水洗牛仔外套，宽松版型。采用优质丹宁面料，耐磨耐穿。百搭款式，四季皆宜。',
            'price': 259.00,
            'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=300&fit=crop',
            'category': 'clothing',
            'stock': 80
        },
        {
            'name': '意式浓缩咖啡机',
            'description': '家用半自动咖啡机，15Bar高压萃取。蒸汽奶泡系统，可制作拿铁、卡布奇诺等。不锈钢机身，易于清洁。',
            'price': 899.00,
            'image_url': 'https://images.unsplash.com/photo-1517914309578-2742d2f0639f?w=400&h=300&fit=crop',
            'category': 'home',
            'stock': 20
        },
        {
            'name': '北欧风台灯',
            'description': '简约北欧设计LED台灯，三档色温可调，无极亮度调节。护眼无频闪，USB充电接口。适合卧室、书房使用。',
            'price': 159.00,
            'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=300&fit=crop',
            'category': 'home',
            'stock': 60
        },
        {
            'name': '机械键盘 RGB',
            'description': '87键机械键盘，青轴/红轴可选。全键无冲，RGB背光支持自定义灯效。PBT键帽，手感舒适持久耐用。',
            'price': 399.00,
            'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop',
            'category': 'electronics',
            'stock': 40
        },
        {
            'name': '便携双肩背包',
            'description': '商务休闲两用双肩包，防水面料。多隔层设计，可容纳15.6英寸笔记本。人体工学背负系统，减轻肩部压力。',
            'price': 199.00,
            'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop',
            'category': 'clothing',
            'stock': 100
        },
        {
            'name': '香薰蜡烛套装',
            'description': '天然大豆蜡香薰蜡烛，3种香型组合。燃烧时间约40小时/罐。无铅棉芯，燃烧干净无黑烟。',
            'price': 129.00,
            'image_url': 'https://images.unsplash.com/photo-1602607683528-e7c1352d7e7a?w=400&h=300&fit=crop',
            'category': 'home',
            'stock': 70
        },
        {
            'name': '无线充电器',
            'description': '15W快充无线充电器，支持多种设备。智能温控，异物检测。简约设计，即放即充。',
            'price': 79.00,
            'image_url': 'https://images.unsplash.com/photo-1586816879360-004f5b0c51e3?w=400&h=300&fit=crop',
            'category': 'electronics',
            'stock': 150
        }
    ]
    
    for product_data in sample_products:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
    print(f"Seeded {len(sample_products)} products to database")
