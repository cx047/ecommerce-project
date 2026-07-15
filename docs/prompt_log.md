# AI 辅助编程记录

这个项目是 AI 辅助编程与工程化实训的考核作业，我使用了 TRAE IDE 内置的 AI 助手来帮助完成。下面是我在开发过程中和 AI 交互的主要记录。

---

## 第1次：确定项目架构

**我的提问**：
> 我要做一个电商全栈项目，考核要求前端至少3个页面、后端至少3个接口。你帮我看看用什么技术栈比较好？

**AI的回复**：
> 建议采用以下架构：
> - 前端：Next.js 14 (App Router) + TypeScript
> - 后端：Flask + Flask-SQLAlchemy + Flask-CORS
> - 数据库：SQLite（开发简便）
>
> 数据库模型设计：
> 1. Product（商品）：id, name, description, price, image_url, category, stock
> 2. CartItem（购物车）：id, product_id, quantity, session_id
> 3. Order（订单）：id, session_id, total_amount, status, customer_name, customer_email
> 4. OrderItem（订单项）：id, order_id, product_id, quantity, price_at_time

**对应文件**：决定了整个项目的技术选型和数据库设计，影响了后续所有代码的编写。

---

## 第2次：写后端代码

**我的提问**：
> 帮我写 Flask 后端，要有商品、购物车、订单这几个功能，数据库用 SQLite。

**AI的回复**（部分关键代码）：

models.py - 数据库模型：
```python
from flask_sqlalchemy import SQLAlchemy

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

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    session_id = db.Column(db.String(100), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    customer_name = db.Column(db.String(100), nullable=True)
    customer_email = db.Column(db.String(100), nullable=True)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
```

app.py - API 路由（节选）：
```python
@app.route('/api/products', methods=['GET'])
def get_products():
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

@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    session_id = get_session_id()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(
        session_id=session_id, product_id=product_id
    ).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(product_id=product_id, quantity=quantity, session_id=session_id)
        db.session.add(cart_item)
    db.session.commit()
    return jsonify({'success': True, 'data': cart_item.to_dict()})
```

**对应文件**：`backend/models.py`、`backend/app.py`、`backend/config.py`、`backend/seed_data.py`

**我的操作**：
代码运行后 API 能正常返回数据。但前端联调时发现 CORS 配置只写了 localhost:3000，前端实际跑在 3001 端口上，我自己手动把 3001 加到 CORS 白名单里才解决。

---

## 第3次：写前端页面

**我的提问**：
> 前端页面帮我写一下，要有首页、商品详情、购物车、订单这几个页面，用 Next.js。

**AI的回复**（部分关键代码）：

lib/api.ts - API 封装：
```typescript
const API_BASE_URL = 'http://127.0.0.1:5000/api';

function getSessionId(): string {
  let sessionId = localStorage.getItem('session_id');
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem('session_id', sessionId);
  }
  return sessionId;
}

async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-Session-ID': getSessionId(),
      ...options.headers,
    },
  });
  return response.json();
}

export function getProducts(category?: string, search?: string) {
  const params = new URLSearchParams();
  if (category) params.append('category', category);
  if (search) params.append('search', search);
  return fetchAPI(`/products${params.toString() ? '?' + params : ''}`);
}

export function addToCart(productId: number, quantity: number = 1) {
  return fetchAPI('/cart', {
    method: 'POST',
    body: JSON.stringify({ product_id: productId, quantity }),
  });
}
```

app/page.tsx - 首页商品列表（节选）：
```tsx
'use client';
import { useState, useEffect } from 'react';
import { getProducts, getCategories, addToCart } from '@/lib/api';

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('');

  useEffect(() => {
    loadProducts();
  }, []);

  async function loadProducts() {
    const result = await getProducts(selectedCategory || undefined);
    setProducts(result.data || []);
  }

  async function handleAddToCart(productId: number) {
    await addToCart(productId, 1);
    window.dispatchEvent(new Event('cartUpdated'));
    alert('已添加到购物车！');
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '24px' }}>
      {products.map((product) => (
        <div key={product.id} className="card">
          <img src={product.image_url} alt={product.name} />
          <h3>{product.name}</h3>
          <p>¥{product.price.toFixed(2)}</p>
          <button onClick={() => handleAddToCart(product.id)}>加入购物车</button>
        </div>
      ))}
    </div>
  );
}
```

**对应文件**：`frontend/app/page.tsx`、`frontend/app/product/[id]/page.tsx`、`frontend/app/cart/page.tsx`、`frontend/app/orders/page.tsx`、`frontend/components/Header.tsx`、`frontend/lib/api.ts`

**我的操作**：
代码跑起来后首页商品列表显示不出来，报"加载商品失败"。排查发现是 CORS 跨域问题。另外购物车数量加减的逻辑 AI 写的有点问题，我自己调整了。订单页的下结算功能也是我根据 API 接口补上的。

---

## 第4次：写文档

**我的提问**：
> 帮我写一下 README 和 API 文档，考核要用。

**AI的回复**（README 节选）：
```markdown
# 优选商城

## 技术栈
- 前端: Next.js 14 + React 18 + TypeScript
- 后端: Flask + Flask-SQLAlchemy + Flask-CORS
- 数据库: SQLite

## 本地开发
cd backend
pip install -r requirements.txt
python app.py

cd frontend
npm install
npm run dev
```

**对应文件**：`README.md`、`docs/API.md`

**我的操作**：
AI 生成的文档基本框架还行，但 API 文档里有些返回值跟实际对不上，我自己修改了。README 里也补充了部署说明部分。

---

## 第5次：代码审查

**我的提问**：
> 你帮我看看代码有没有什么明显的问题？

**AI的回复**：
> 1. 项目结构清晰，前后端分离做得不错
> 2. 建议添加输入验证（如 marshmallow 或 pydantic）
> 3. 建议添加请求频率限制
> 4. 建议前端添加错误边界（Error Boundary）
> 5. 建议为数据库常用查询字段添加索引
> 6. 建议添加单元测试

**对应文件**：`docs/code_review.md`

**我的操作**：
这些建议确实有用，但时间比较紧先没加。我把审查结果整理成了 code_review.md 提交上去了。

---

## 使用 AI 的感受

| 方面 | 评价 |
|------|------|
| 代码生成速度 | 很快，几分钟就能生成一套完整的代码框架 |
| 代码质量 | 整体还行，但有些地方需要自己调整 |
| 遇到的问题 | CORS 配置、API 调用封装这些细节容易出错 |
| 我的工作量 | 大概 60% AI 生成，40% 自己调试修改 |

**个人体会**：
AI 确实能提高开发效率，特别是搭建项目骨架的时候。但完全依赖 AI 是不行的，出了问题还是得自己排查。比如 CORS 那个问题，AI 生成的配置没考虑到端口变化，是我自己在测试时发现的。还有就是业务逻辑比较复杂的部分（比如购物车数量联动、订单状态流转），AI 生成的代码有时候不够完善，需要手动调整。总的来说，AI 是一个很好的辅助工具，但开发者自己的思考和调试能力还是最重要的。