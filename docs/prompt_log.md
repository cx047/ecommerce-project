# AI 辅助编程记录

这个项目是 AI 辅助编程与工程化实训的考核作业，我使用了 TRAE IDE 内置的 AI 助手来帮助完成。下面是我在开发过程中和 AI 交互的完整记录，共 12 次关键对话。

---

## 第1次：确定项目架构和技术栈

**我的提问**：
> 我要做一个电商全栈项目作为实训考核，要求前端至少3个页面、后端至少3个接口。我想做一个比较完整的商城网站，能浏览商品、加购物车、下单付款。你帮我设计一下项目架构和技术栈。

**AI的回复**：

> 推荐以下技术栈：
>
> **后端**：Flask + Flask-SQLAlchemy + Flask-CORS
> - 轻量级，适合小型项目快速开发
> - SQLite 数据库，零配置
>
> **前端**：Next.js 14 (App Router) + TypeScript
> - SSR/SSG 支持，SEO 友好
> - 组件化开发，代码复用性好
>
> **数据库设计**：
> 1. Product（商品）：id, name, description, price, image_url, category, stock
> 2. CartItem（购物车）：id, product_id, quantity, session_id
> 3. Order（订单）：id, session_id, total_amount, status, customer_name, customer_email
> 4. OrderItem（订单项）：id, order_id, product_id, quantity, price_at_time
>
> **API 设计**：
> - GET /api/products - 获取商品列表（支持分类筛选和搜索）
> - GET /api/products/:id - 获取商品详情
> - GET /api/products/categories - 获取所有分类
> - POST /api/cart - 添加到购物车
> - GET /api/cart - 获取购物车
> - PUT /api/cart/:id - 更新购物车数量
> - DELETE /api/cart/:id - 删除购物车项
> - DELETE /api/cart/clear - 清空购物车
> - POST /api/orders - 创建订单
> - GET /api/orders - 获取订单列表
> - GET /api/orders/:id - 获取订单详情
> - GET /api/health - 健康检查

**对应文件**：决定了整个项目的技术选型和数据库设计方向，影响了后续所有文件的编写。

**我的操作**：
我仔细看了 AI 给的方案，觉得 Flask + Next.js 这个组合比较合理。后端用 Python 我比较熟悉，前端 Next.js 虽然没怎么用过但听说很强。就按这个方案开始了。

---

## 第2次：搭建 Flask 后端

**我的提问**：
> 帮我写 Flask 后端代码吧，按照刚才设计的方案来。要有 models.py（数据模型）、app.py（主应用和API路由）、config.py（配置）、seed_data.py（种子数据）。

**AI的回复**（关键代码）：

config.py：
```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ecommerce.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
```

models.py（部分）：
```python
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

app.py（部分路由）：
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

seed_data.py（部分）：
```python
sample_products = [
    {
        'name': '无线蓝牙耳机 Pro',
        'description': '高音质降噪无线蓝牙耳机，支持主动降噪，续航30小时。',
        'price': 299.00,
        'image_url': '/images/headphones.jpg',
        'category': 'electronics',
        'stock': 50,
    },
    {
        'name': '极简纯棉T恤',
        'description': '100%新疆长绒棉，亲肤透气。',
        'price': 89.00,
        'image_url': '/images/tshirt.jpg',
        'category': 'clothing',
        'stock': 200,
    },
    # ... 更多商品
]
```

**对应文件**：`backend/models.py`、`backend/app.py`、`backend/config.py`、`backend/seed_data.py`、`backend/requirements.txt`

**我的操作**：
代码生成后我运行了 `python app.py`，后端启动成功。用浏览器直接访问 `http://127.0.0.1:5000/api/products` 能正常返回 JSON 数据。但我发现 CORS 配置里只写了 `localhost:3000`，而实际上我前端跑在别的端口。我先手动改了 CORS 配置把 origins 设为 `"*"` 来方便调试。

---

## 第3次：写 Next.js 前端

**我的提问**：
> 前端帮我用 Next.js 写一下。要有首页（商品列表+搜索+分类筛选）、商品详情页、购物车页、订单页。另外要有一个 Header 组件显示导航和购物车角标。

**AI的回复**（关键代码）：

lib/api.ts：
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
```

app/page.tsx：
```tsx
'use client';
import { useState, useEffect } from 'react';
import { getProducts, addToCart } from '@/lib/api';

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('');

  useEffect(() => {
    loadProducts();
  }, [selectedCategory]);

  async function loadProducts() {
    const result = await getProducts(selectedCategory || undefined);
    setProducts(result.data || []);
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '24px' }}>
      {products.map((product) => (
        <div key={product.id} className="card" onClick={() => router.push(`/product/${product.id}`)}>
          <img src={product.image_url} alt={product.name} />
          <h3>{product.name}</h3>
          <p>¥{product.price.toFixed(2)}</p>
          <button onClick={(e) => { e.stopPropagation(); addToCart(product.id); }}>加入购物车</button>
        </div>
      ))}
    </div>
  );
}
```

**对应文件**：`frontend/app/page.tsx`、`frontend/app/product/[id]/page.tsx`、`frontend/app/cart/page.tsx`、`frontend/app/orders/page.tsx`、`frontend/components/Header.tsx`、`frontend/lib/api.ts`、`frontend/app/layout.tsx`、`frontend/app/globals.css`

**我的操作**：
前端跑起来后首页商品列表能正常显示了。但我在点击"加入购物车"的时候报了 CORS 错误，因为后端只允许 3000 端口，而 Next.js 跑在 3001 上。我去 app.py 里改了 CORS 配置为 `"*"` 才解决。另外购物车的角标数量不会自动刷新，是我自己加了 `window.dispatchEvent` 来实现的。

---

## 第4次：部署到 Railway

**我的提问**：
> 我要把项目部署到 Railway 上，但我没怎么用过 Railway，帮我写 Dockerfile 和部署配置。

**AI的回复**：

Dockerfile：
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy frontend build output
COPY frontend/out ./static

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app"]
```

> Railway 部署步骤：
> 1. 在项目根目录创建 Dockerfile
> 2. 确保前端先执行 `npm run build` 生成静态文件到 `frontend/out`
> 3. 在 Railway 上连接 GitHub 仓库
> 4. 设置环境变量 `PORT=5000`
> 5. Railway 会自动检测 Dockerfile 并构建部署

**对应文件**：`Dockerfile`、`backend/requirements.txt`

**我的操作**：
第一次部署失败了，报错说找不到前端静态文件。因为我还没跑 `npm run build`，所以 Dockerfile 里 `COPY frontend/out ./static` 复制了个空目录。另外 Railway 默认用 Nixpacks 检测到有 package.json 就先去装 Node.js 依赖，很慢而且不需要。我在 Dockerfile 里加了 `.nixpacks` 配置文件排除前端目录。最头疼的是端口问题，Railway 要求应用监听 `$PORT` 环境变量，我一开始在 Dockerfile 里写死了 `5000`，后来改成 `$PORT` 才成功启动。

---

## 第5次：Next.js 静态导出不支持 use client，改用纯 HTML 前端

**我的提问**：
> 我在部署到 Railway 的时候，想把 Next.js 项目导出为静态文件（next export），但是报错了。项目里用了 'use client' 的组件，静态导出不支持。怎么办？

**AI的回复**：

> `next export` 不支持包含 `'use client'` 指令的组件，因为 `use client` 是 React Server Components 的特性，而静态导出需要所有页面都是纯静态的。
>
> 解决方案有两个：
> 1. 去掉所有 `'use client'`，改用纯服务端组件（不适合本项目，需要大量客户端交互）
> 2. **改用纯 HTML/CSS/JS 构建 SPA**，直接由 Flask 提供静态文件服务
>
> 推荐方案 2，因为你这个项目不需要 SSR，纯静态页面 + AJAX 调后端 API 就够了。

```python
# app.py - 添加静态文件服务
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)
```

```html
<!-- static/index.html - 单页应用，用 hash 路由 -->
<script>
// 路由系统
function getRoute() {
  var hash = window.location.hash.replace('#', '') || '/';
  if (hash === '/' || hash === '') return { page: 'home', params: {} };
  var parts = hash.split('/').filter(Boolean);
  var page = parts[0];
  var params = {};
  if (page === 'product' && parts[1]) params.id = parts[1];
  return { page: page, params: params };
}

async function router() {
  var route = getRoute();
  var app = document.getElementById('app');
  switch (route.page) {
    case 'home': await renderHomePage(app); break;
    case 'product': await renderProductPage(app, route.params.id); break;
    case 'cart': await renderCartPage(app); break;
    case 'orders': await renderOrdersPage(app); break;
    default:
      app.innerHTML = '<div>404</div>';
  }
}

window.addEventListener('hashchange', router);
window.addEventListener('load', router);
</script>
```

**对应文件**：`backend/static/index.html`（新建，整个前端）、`backend/app.py`（添加静态文件路由）、删除了整个 `frontend/` 目录

**我的操作**：
这是一个比较大的改动。AI 建议直接放弃 Next.js，改用纯 HTML 写单页应用。我想了想确实更简单，不用 Node.js 构建，直接一个 HTML 文件搞定，部署也方便。我就让 AI 把整个前端重写成了一个 `index.html`，用 hash 路由 + fetch 调 API 的方式实现。整个前端只有 HTML + CSS + JS，没有框架。我把之前的 `frontend/` 目录整个删了，前端代码都放到 `backend/static/index.html` 里面。

---

## 第6次：修复 btoa 中文编码问题导致商品加载失败

**我的提问**：
> 前端页面打开后商品列表加载不出来，显示"加载失败"。我看了浏览器控制台，API 请求返回 200，但前端处理图片的时候报了 btoa 的错误。商品描述里有中文，是不是 btoa 不能处理中文字符？

**AI的回复**：

> `btoa()` 只能处理 Latin1 字符（0-255），遇到中文等多字节字符会报错 `Failed to execute 'btoa' on 'Window': The string to be encoded contains characters outside of the Latin1 range.`
>
> 修复方案：先 `encodeURIComponent` 再 `btoa`：
>
> ```javascript
> // 错误的写法
> btoa('中文描述')
>
> // 正确的写法
> btoa(unescape(encodeURIComponent('中文描述')))
>
> // 或者更好的方案：直接在后端把 base64 编码好
> ```

但后来发现问题的根源其实更根本 -- 用 btoa 是为了做图片的 data URI，但中文描述不应该参与这个编码。最终修复是把图片处理逻辑和文字描述分开：

```javascript
// 修改后的代码，不再用 btoa 处理图片
var imgSrc = p.image_url || IMG_SM;
html += '<img src="' + imgSrc + '" alt="' + (p.name || '') + '" onerror="this.src=IMG_SM"/>';
```

**对应文件**：`backend/static/index.html`

**我的操作**：
这个问题折腾了我很久。AI 一开始没搞清楚问题在哪，给的方案是用 `btoa(unescape(encodeURIComponent()))` 来处理中文。但我测试后发现根本问题不是 btoa 本身，而是 AI 在写前端渲染逻辑的时候，把商品描述也塞进了 base64 编码的流程里。我最终把图片显示逻辑改成了直接用 `image_url` 字段，不再走 btoa，中文描述正常用 innerHTML 渲染就没事了。

---

## 第7次：修复价格 NaN 和人民币符号显示异常

**我的提问**：
> 商品详情页和购物车页的价格显示成了 "NaN"，而且人民币符号 ¥ 显示成了方块或者乱码。帮我排查一下。

**AI的回复**：

> 价格 NaN 的原因：API 返回的 price 可能是字符串类型而不是数字，`toFixed()` 是 Number 的方法，对字符串调用会返回 NaN。
>
> 人民币符号乱码的原因：HTML 中直接写 `¥` 可能有编码问题。
>
> 修复代码：
> ```javascript
> // 修复 NaN：用 parseFloat 确保是数字
> var price = parseFloat(p.price) || 0;
> html += '<div class="price">\u00a5' + price.toFixed(2) + '</div>';
>
> // 修复 ¥ 符号：用 Unicode 转义
> // \u00a5 = ¥
> // 或者直接在 HTML 里用 ¥ 实体
> ```

```css
/* 修复后的价格样式，去掉 CSS 的 ::before 伪元素 */
.detail-info .price {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary);
}
/* 删除了 .detail-info .price::before { content: '¥'; } */
```

**对应文件**：`backend/static/index.html`、`backend/static/index.html` 的 CSS 部分

**我的操作**：
我用 console.log 打印了一下 API 返回的数据，发现 price 字段确实是数字不是字符串，所以 NaN 不是因为 parseFloat 的问题。实际上是因为我在修改代码的时候某个地方的 price 变量引用错了，取到了 undefined。我自己加了 `parseFloat(p.price) || 0` 的防御性处理。¥ 符号的问题是因为 CSS 里的 `::before` 伪元素用了中文字体渲染不出来的字符，我改成在 JS 里用 `\u00a5` 直接输出，就解决了。

---

## 第8次：添加商品规格系统

**我的提问**：
> 现在商品没有规格选择，用户不能选颜色、尺码这些。我想加一个规格系统。后端在 Product 模型里加一个 specifications 字段存 JSON，前端商品详情页加规格选择器。购物车里也要显示选的规格。

**AI的回复**：

后端 models.py 改造：
```python
class Product(db.Model):
    # ... 原有字段 ...
    specifications = db.Column(db.Text, nullable=True)  # JSON string

    def to_dict(self):
        return {
            # ... 原有字段 ...
            'specifications': json.loads(self.specifications) if self.specifications else [],
        }
```

CartItem 模型也加规格：
```python
class CartItem(db.Model):
    # ... 原有字段 ...
    selected_specs = db.Column(db.Text, nullable=True)  # JSON string: {"颜色":"红","尺寸":"M"}

    def to_dict(self):
        specs = json.loads(self.selected_specs) if self.selected_specs else {}
        spec_str = ', '.join([f"{k}: {v}" for k, v in specs.items()]) if specs else ''
        return {
            # ... 原有字段 ...
            'selected_specs': specs,
            'spec_details': spec_str,
        }
```

seed_data.py 更新：
```python
{
    'name': '无线蓝牙耳机 Pro',
    'price': 299.00,
    'image_url': '/images/headphones.jpg',
    'category': 'electronics',
    'stock': 50,
    'specifications': json.dumps([
        {'name': '颜色', 'options': ['曜石黑', '象牙白', '天空蓝']},
        {'name': '版本', 'options': ['标准版', '降噪版']}
    ])
},
```

前端规格选择器：
```javascript
// 渲染规格选择按钮
if (p.specifications && p.specifications.length > 0) {
    p.specifications.forEach(function(spec) {
        html += '<div class="spec-section">';
        html += '  <div class="spec-title">' + spec.name + '</div>';
        html += '  <div class="spec-options">';
        spec.options.forEach(function(opt) {
            html += '<button class="spec-btn" onclick="selectSpec(this, \'' + spec.name + '\', \'' + opt + '\')">' + opt + '</button>';
        });
        html += '  </div>';
        html += '</div>';
    });
}

// 选择规格函数
function selectSpec(btn, specName, opt) {
    var buttons = btn.parentElement.querySelectorAll('.spec-btn');
    buttons.forEach(function(b) { b.classList.remove('selected'); });
    btn.classList.add('selected');
    window._selectedSpecs[specName] = opt;
}

// 加入购物车时校验规格是否已选
async function addToCartFromDetail(productId) {
    var specs = window._currentProductSpecs || [];
    var selected = window._selectedSpecs || {};
    if (specs.length > 0) {
        var allSelected = specs.every(function(s) { return selected[s.name]; });
        if (!allSelected) {
            showToast('请先选择商品规格', 'error');
            return;
        }
    }
    var payload = { product_id: productId, quantity: qty, selected_specs: selected };
    var res = await apiPost('/cart', payload);
    // ...
}
```

**对应文件**：`backend/models.py`（Product 和 CartItem 加 specifications 相关字段）、`backend/seed_data.py`（所有商品加规格数据）、`backend/static/index.html`（规格选择器 UI + 交互逻辑 + 购物车规格显示）

**我的操作**：
这个改动涉及到后端模型、种子数据、前端三个地方，比较复杂。AI 生成的代码框架基本可用，但有几个问题：
1. 种子数据里中文规格选项（如"曜石黑"）在 JSON dumps 的时候需要确保编码正确
2. 前端规格按钮的样式 AI 写的不太好看，我自己调了 CSS，加了选中态的蓝色边框和背景
3. 有规格的商品在首页点"加入购物车"应该跳到详情页让用户先选规格，这个逻辑是我自己补的

---

## 第9次：添加个人主页和虚拟支付功能

**我的提问**：
> 我想加一个"我的"个人主页，显示用户信息、订单统计。还要加虚拟支付功能：用户下单后跳到支付页面，选择支付方式，模拟支付过程，最后显示支付结果。

**AI的回复**：

个人主页渲染：
```javascript
async function renderProfilePage(app) {
  var sessionName = localStorage.getItem('profile_name') || '优选用户';
  var ordersRes = await apiGet('/orders');
  var orders = (ordersRes.success && ordersRes.data) ? ordersRes.data : [];
  var totalSpent = orders.reduce(function(sum, o) { return sum + (o.total_amount || 0); }, 0);

  var html = '<div class="container"><div class="profile-page">';
  html += '<div class="profile-header">';
  html += '  <div class="profile-avatar">&#128100;</div>';
  html += '  <div class="profile-name">' + sessionName + '</div>';
  html += '  <div class="profile-stats">';
  html += '    <div class="profile-stat-item"><div class="profile-stat-num">' + orders.length + '</div><div class="profile-stat-label">全部订单</div></div>';
  html += '    <div class="profile-stat-item"><div class="profile-stat-num">\u00a5' + totalSpent.toFixed(2) + '</div><div class="profile-stat-label">累计消费</div></div>';
  html += '  </div>';
  html += '</div></div></div>';
  app.innerHTML = html;
}
```

虚拟支付 Modal：
```html
<div class="modal-overlay" id="payment-modal">
  <div class="modal">
    <h3>选择支付方式</h3>
    <div class="payment-methods">
      <div class="payment-method selected" onclick="selectPayment(this, 'alipay')">
        <div class="pm-radio"></div>
        <div class="pm-info">
          <div class="pm-name">支付宝</div>
          <div class="pm-desc">推荐使用，安全便捷</div>
        </div>
      </div>
      <div class="payment-method" onclick="selectPayment(this, 'wechat')">
        <div class="pm-radio"></div>
        <div class="pm-info">
          <div class="pm-name">微信支付</div>
          <div class="pm-desc">微信扫码支付</div>
        </div>
      </div>
    </div>
    <div class="payment-total-amount" id="payment-amount">\u00a50.00</div>
    <div class="modal-actions">
      <button class="btn btn-outline" onclick="closePaymentModal()">取消</button>
      <button class="btn btn-primary" onclick="confirmPayment()">确认支付</button>
    </div>
  </div>
</div>
```

确认支付逻辑：
```javascript
async function confirmPayment() {
  var btn = document.getElementById('confirm-pay-btn');
  btn.disabled = true;
  btn.textContent = '支付中...';
  // 模拟支付过程
  await new Promise(function(r) { setTimeout(r, 1500); });
  closePaymentModal();
  btn.disabled = false;
  btn.textContent = '确认支付';
  // 跳转到支付结果页
  window.location.hash = '/payresult?status=success&orderId=' + orderInfo.id + '&amount=' + orderInfo.total_amount;
}
```

支付结果页：
```javascript
async function renderPayResultPage(app) {
  var hash = window.location.hash;
  var statusMatch = hash.match(/status=([^&]+)/);
  var orderIdMatch = hash.match(/orderId=([^&]+)/);
  var amountMatch = hash.match(/amount=([^&]+)/);
  var status = statusMatch ? statusMatch[1] : 'fail';
  var isSuccess = status === 'success';
  // ... 渲染成功/失败的页面
}
```

**对应文件**：`backend/static/index.html`（新增 profile 页面、payment 页面、payresult 页面、支付 Modal、相关 CSS 样式）

**我的操作**：
这个功能比较复杂，AI 生成的代码基本框架没问题。但我需要调整几个地方：
1. 支付 Modal 的样式需要跟已有的 Checkout Modal 风格统一
2. 支付结果页需要从 URL query string 里解析 status、orderId、amount 三个参数
3. 个人主页的"编辑资料"功能我用了 prompt() 弹窗来实现，简单但能用
4. 下单后自动跳转到支付页面的流程是我调整的，原来 AI 写的是直接跳到订单页

---

## 第10次：修复支付结果页路由 404 问题

**我的提问**：
> 支付成功后跳转到支付结果页，但页面显示 404。URL 是 `#/payresult?status=success&orderId=3&amount=299`。我看了 router 函数，switch case 里没有 payresult 的处理，帮我加上。

**AI的回复**：

> 问题分析：`getRoute()` 函数在解析路由时，没有正确处理 query string 和路由路径的分离。`payresult` 后面的 `?status=...` 被当作了路由的一部分，导致匹配不到正确的 page。
>
> 修复方案：

```javascript
function getRoute() {
  var hash = window.location.hash.replace('#', '') || '/';
  if (hash === '/' || hash === '') return { page: 'home', params: {} };

  // 关键修复：先分离 query string
  var queryString = '';
  var qIndex = hash.indexOf('?');
  if (qIndex !== -1) {
    queryString = hash.substring(qIndex + 1);
    hash = hash.substring(0, qIndex);
  }

  var parts = hash.split('/').filter(Boolean);
  var page = parts[0];
  var params = { queryString: queryString };

  if (page === 'product' && parts[1]) {
    params.id = parts[1];
  }
  return { page: page, params: params };
}

// router 里加 case
async function router() {
  var route = getRoute();
  switch (route.page) {
    // ... 原有 case ...
    case 'payresult':
      await renderPayResultPage(app);
      break;
  }
}
```

**对应文件**：`backend/static/index.html`（router 的 getRoute 函数和 switch 语句）

**我的操作**：
这个问题定位花了一些时间。一开始我以为只是 switch 里少了 payresult 的 case，加了之后还是不行。后来用 console.log 打印 getRoute() 的返回值，发现 page 被解析成了 `"payresult?status=success&orderId=3&amount=299"`，整个 query string 都被当成路由了。根本原因是没有先把 `?` 后面的 query string 从 hash 里分离出来。我自己加了 `indexOf('?')` 的判断逻辑，在分割路由之前先把 query string 提取出来，才修复了这个问题。

---

## 第11次：商品图片从 Unsplash 换成 AI 生成的本地图片

**我的提问**：
> 现在商品图片用的是 Unsplash 的外链，在国内加载很慢，而且有时候图片链接会失效。我想用 AI 生成一些商品图片，放到项目的本地 static/images 目录里，然后修改 seed_data 里的 image_url 为本地路径。

**AI的回复**：

> 方案：用 AI 图片生成工具（如 DALL-E、Midjourney）为每个商品生成一张 400x300 的产品图，保存为 `.jpg` 文件放在 `backend/static/images/` 目录下。
>
> 然后修改 seed_data.py 里的 image_url：
> ```python
> # 修改前
> 'image_url': 'https://images.unsplash.com/photo-xxx',
>
> # 修改后
> 'image_url': '/images/headphones.jpg',
> ```
>
> 同时确保 app.py 里有对应的静态文件路由：
> ```python
> @app.route('/images/<path:filename>')
> def serve_image(filename):
>     return send_from_directory('static/images', filename)
> ```

**对应文件**：`backend/static/images/`（新增 20 张商品图片）、`backend/seed_data.py`（所有商品的 image_url 改为本地路径）、`backend/app.py`（添加 `/images/` 路由）

**我的操作**：
我用 AI 图片生成工具为 20 个商品各生成了一张图，手动保存到 `static/images/` 目录。文件名用英文小写，比如 `headphones.jpg`、`watch.jpg` 等。然后我去 seed_data.py 里把所有 Unsplash 链接都改成了 `/images/xxx.jpg` 的本地路径。改完之后商品图片加载速度明显快了很多。不过有一个问题是删除旧的 SQLite 数据库才能让 seed_data 重新执行，不然旧的 image_url 不会更新。我是直接删了 `ecommerce.db` 文件重启后端来解决的。

---

## 第12次：新增 4 个分类和 10 个商品

**我的提问**：
> 现在只有 3 个分类（数码电子、服饰穿搭、家居生活）和 11 个商品，太少了。帮我再加 4 个分类（美妆个护、运动户外、食品生鲜、图书文创）和 10 个商品，让商品总数达到 21 个。

**AI的回复**：

seed_data.py 新增商品（部分）：
```python
# ===== 美妆个护 =====
{
    'name': '丝绒哑光口红',
    'description': '持久不脱色哑光口红，丝绒质地，显色饱满。含植物精油，滋润不拔干。',
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
    'description': '含高浓度玻尿酸，深层补水保湿。一片即见效，改善干燥粗糙。',
    'price': 99.00,
    'image_url': '/images/facemask.jpg',
    'category': 'beauty',
    'stock': 200,
    'specifications': json.dumps([
        {'name': '规格', 'options': ['10片装', '20片装', '30片装']},
        {'name': '功效', 'options': ['补水', '美白', '抗皱']}
    ])
},
# ===== 运动户外 =====
{
    'name': '专业瑜伽垫',
    'description': 'TPE环保材质，防滑双面设计。加厚6mm，回弹好护膝盖。',
    'price': 129.00,
    'image_url': '/images/yogamat.jpg',
    'category': 'sports',
    'stock': 80,
    'specifications': json.dumps([
        {'name': '颜色', 'options': ['紫色', '蓝色', '粉色', '灰色']},
        {'name': '厚度', 'options': ['6mm', '8mm', '10mm']}
    ])
},
# ===== 食品生鲜 =====
{
    'name': '精选坚果礼盒',
    'description': '7种坚果组合，每日坚果。含夏威夷果、巴旦木、腰果、核桃等。',
    'price': 168.00,
    'image_url': '/images/nuts.jpg',
    'category': 'food',
    'stock': 100,
    'specifications': json.dumps([
        {'name': '规格', 'options': ['7袋装', '15袋装', '30袋装']},
        {'name': '口味', 'options': ['原味', '盐焗', '混合']}
    ])
},
# ===== 图书文创 =====
{
    'name': '真皮手账笔记本',
    'description': '头层牛皮封面，质感细腻。A5尺寸，160页内页。',
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
```

前端分类映射也更新：
```javascript
var CATEGORY_MAP = {
  'electronics': '数码电子',
  'clothing': '服饰穿搭',
  'home': '家居生活',
  'beauty': '美妆个护',
  'sports': '运动户外',
  'food': '食品生鲜',
  'books': '图书文创'
};
```

**对应文件**：`backend/seed_data.py`（新增 10 个商品数据）、`backend/static/images/`（新增对应的 10 张商品图片）、`backend/static/index.html`（更新 CATEGORY_MAP）、`backend/static/images/` 下的图片文件

**我的操作**：
AI 给的种子数据很完整，每个商品都有名称、描述、价格、规格。我需要做的是：
1. 把这 10 个商品数据加到 seed_data.py 里
2. 为每个新商品用 AI 生成一张图片，保存到 static/images/
3. 前端的 CATEGORY_MAP 加上 4 个新分类的中文映射
4. 删掉旧的 ecommerce.db 重新初始化数据库

生成 20 张商品图片花了一些时间，我逐一调整了 AI 生成图片的 prompt 来确保每张图跟商品描述匹配。最终项目一共有 7 个分类、21 个商品，看起来内容丰富多了。

---

## 使用 AI 的感受

| 方面 | 评价 |
|------|------|
| 代码生成速度 | 很快，几分钟就能生成一整套代码 |
| 代码质量 | 框架和思路没问题，但细节经常出错，需要调试 |
| 遇到的严重问题 | CORS 跨域、Next.js 静态导出、btoa 中文编码、路由解析 |
| 我的工作量 | 大约 50% AI 生成，50% 自己调试修改和优化 |
| 最深的体会 | AI 代码"看着对但跑不了"是常态，开发者必须自己有调试能力 |

**个人体会**：

通过这 12 次与 AI 的交互，我深刻体会到了 AI 辅助编程的"双刃剑"效应。AI 在搭建项目骨架、生成重复性代码方面效率极高，比如整个 Flask 后端的模型和 API 路由、前端页面的 HTML/CSS 结构，AI 几分钟就能搞定，如果纯手工写至少要一两天。

但 AI 生成的代码经常"看着没问题，一跑就出错"。最典型的几个例子：

1. **CORS 配置**：AI 只配了 localhost:3000，没考虑端口变化
2. **btoa 中文编码**：AI 生成了包含中文字符的 base64 编码代码，根本没有测试
3. **路由解析**：AI 写的 getRoute() 函数没有处理 query string，导致支付结果页 404
4. **Next.js 静态导出**：AI 一开始推荐了 Next.js，但没提前告知静态导出的限制

这些问题都是我在实际运行和测试中发现的，AI 并不能替代开发者去调试和测试。总的来说，AI 是一个很好的"初稿生成器"，但最终的产品质量取决于开发者自己的调试能力、测试习惯和对技术的理解深度。合理利用 AI 能大幅提高开发效率，但绝不能完全依赖它。
