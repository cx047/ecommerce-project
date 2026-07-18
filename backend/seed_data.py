from models import db, Product
import json

def seed_database():
    """Seed the database with sample products if empty"""
    if Product.query.first():
        return  # Database already has data

    sample_products = [
        {
            'name': '无线蓝牙耳机 Pro',
            'description': '高音质降噪无线蓝牙耳机，支持主动降噪，续航30小时，IPX7防水等级。采用最新蓝牙5.3技术，连接稳定低延迟。',
            'price': 299.00,
            'image_url': '/images/headphones.jpg',
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
            'image_url': '/images/watch.jpg',
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
            'image_url': '/images/tshirt.jpg',
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
            'image_url': '/images/jacket.jpg',
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
            'image_url': '/images/coffee.jpg',
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
            'image_url': '/images/lamp.jpg',
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
            'image_url': '/images/keyboard.jpg',
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
            'image_url': '/images/backpack.jpg',
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
            'image_url': '/images/candle.jpg',
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
            'image_url': '/images/charger.jpg',
            'category': 'electronics',
            'stock': 150,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['白色', '黑色']},
                {'name': '功率', 'options': ['10W', '15W']}
            ])
        },
        # ===== 美妆个护 =====
        {
            'name': '丝绒哑光口红',
            'description': '持久不脱色哑光口红，丝绒质地，显色饱满。含植物精油，滋润不拔干。多种色号可选，适合各种肤色。',
            'price': 149.00,
            'image_url': '/images/lipstick.jpg',
            'category': 'beauty',
            'stock': 120,
            'specifications': json.dumps([
                {'name': '色号', 'options': ['正红', '豆沙', '枫叶红', '姨妈红']},
                {'name': '质地', 'options': ['哑光', '滋润']}
            ])
        },
        {
            'name': '玻尿酸保湿面膜套装',
            'description': '含高浓度玻尿酸，深层补水保湿。一片即见效，改善干燥粗糙。温和无刺激，适合敏感肌。',
            'price': 99.00,
            'image_url': '/images/facemask.jpg',
            'category': 'beauty',
            'stock': 200,
            'specifications': json.dumps([
                {'name': '规格', 'options': ['10片装', '20片装', '30片装']},
                {'name': '功效', 'options': ['补水', '美白', '抗皱']}
            ])
        },
        {
            'name': '优雅女士香水',
            'description': '法式调香，前调柑橘清新，中调花香优雅，后调木质温暖。留香持久8小时，适合日常和约会。',
            'price': 359.00,
            'image_url': '/images/perfume.jpg',
            'category': 'beauty',
            'stock': 45,
            'specifications': json.dumps([
                {'name': '容量', 'options': ['30ml', '50ml', '100ml']},
                {'name': '香调', 'options': ['花香', '果香', '木质']}
            ])
        },
        # ===== 运动户外 =====
        {
            'name': '专业瑜伽垫',
            'description': 'TPE环保材质，防滑双面设计。加厚6mm，回弹好护膝盖。自带绑带，携带方便。适合瑜伽、普拉提。',
            'price': 129.00,
            'image_url': '/images/yogamat.jpg',
            'category': 'sports',
            'stock': 80,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['紫色', '蓝色', '粉色', '灰色']},
                {'name': '厚度', 'options': ['6mm', '8mm', '10mm']}
            ])
        },
        {
            'name': '保温运动水壶',
            'description': '316不锈钢内胆，12小时保温保冷。500ml大容量，一键弹盖，便携挂绳。防漏设计，运动出行必备。',
            'price': 89.00,
            'image_url': '/images/waterbottle.jpg',
            'category': 'sports',
            'stock': 150,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['深蓝', '墨绿', '橙色', '白色']},
                {'name': '容量', 'options': ['500ml', '750ml', '1000ml']}
            ])
        },
        # ===== 食品生鲜 =====
        {
            'name': '精选坚果礼盒',
            'description': '7种坚果组合，每日坚果。含夏威夷果、巴旦木、腰果、核桃等。独立小包装，新鲜锁味。送礼自用两相宜。',
            'price': 168.00,
            'image_url': '/images/nuts.jpg',
            'category': 'food',
            'stock': 100,
            'specifications': json.dumps([
                {'name': '规格', 'options': ['7袋装', '15袋装', '30袋装']},
                {'name': '口味', 'options': ['原味', '盐焗', '混合']}
            ])
        },
        {
            'name': '精品手冲咖啡豆',
            'description': '埃塞俄比亚耶加雪菲，水洗处理。柑橘花香，酸质明亮。中度烘焙，适合手冲。250g真空包装，新鲜烘焙。',
            'price': 88.00,
            'image_url': '/images/coffeebeans.jpg',
            'category': 'food',
            'stock': 90,
            'specifications': json.dumps([
                {'name': '产地', 'options': ['耶加雪菲', '哥伦比亚', '曼特宁']},
                {'name': '烘焙度', 'options': ['浅烘', '中烘', '深烘']},
                {'name': '规格', 'options': ['250g', '500g', '1kg']}
            ])
        },
        # ===== 图书文创 =====
        {
            'name': '真皮手账笔记本',
            'description': '头层牛皮封面，质感细腻。A5尺寸，160页内页。方格/横线/空白可选，平摊书写。附赠书签带和笔扣。',
            'price': 118.00,
            'image_url': '/images/notebook.jpg',
            'category': 'books',
            'stock': 70,
            'specifications': json.dumps([
                {'name': '颜色', 'options': ['棕色', '黑色', '墨绿']},
                {'name': '内页', 'options': ['横线', '方格', '空白']},
                {'name': '尺寸', 'options': ['A6', 'A5', 'B5']}
            ])
        },
        {
            'name': '奢华金尖钢笔',
            'description': '14K金尖，书写顺滑流畅。树脂笔身，金属拉丝工艺。旋转吸墨，附赠墨囊。礼盒包装，适合商务馈赠。',
            'price': 288.00,
            'image_url': '/images/pen.jpg',
            'category': 'books',
            'stock': 50,
            'specifications': json.dumps([
                {'name': '笔尖', 'options': ['EF尖', 'F尖', 'M尖']},
                {'name': '颜色', 'options': ['黑色', '酒红', '藏青']}
            ])
        },
        {
            'name': '青花瓷茶具套装',
            'description': '景德镇青花瓷，一壶四杯。含茶壶1把、品茗杯4只、公道杯1只。高温烧制，釉面光润。送礼收藏佳品。',
            'price': 398.00,
            'image_url': '/images/teapot.jpg',
            'category': 'home',
            'stock': 30,
            'specifications': json.dumps([
                {'name': '套装', 'options': ['一壶四杯', '一壶六杯', '功夫茶套装']},
                {'name': '花色', 'options': ['青花', '粉彩', '素白']}
            ])
        }
    ]

    for product_data in sample_products:
        product = Product(**product_data)
        db.session.add(product)

    db.session.commit()
    print(f"Seeded {len(sample_products)} products to database")
