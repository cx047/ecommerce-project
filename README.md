# 优选商城 - AI辅助编程与工程化实训项目

一个全栈电商应用，包含商品展示、购物车、订单管理等完整功能。

## 技术栈

- **前端**: Next.js 14 + React 18 + TypeScript
- **后端**: Flask + Flask-SQLAlchemy + Flask-CORS
- **数据库**: SQLite
- **部署**: 前端静态部署 + 后端云服务部署

## 功能特性

### 前端页面（4个独立路由）
1. **首页** (`/`) - 商品列表展示、分类筛选、搜索功能
2. **商品详情** (`/product/[id]`) - 商品详细信息、数量选择、加入购物车
3. **购物车** (`/cart`) - 购物车管理、数量调整、结算下单
4. **订单页** (`/orders`) - 订单历史查看、订单详情

### 后端API（8个接口）
1. `GET /api/products` - 获取商品列表（支持分类筛选和搜索）
2. `GET /api/products/<id>` - 获取商品详情
3. `GET /api/products/categories` - 获取商品分类
4. `GET /api/cart` - 获取购物车
5. `POST /api/cart` - 添加商品到购物车
6. `PUT /api/cart/<id>` - 更新购物车商品数量
7. `DELETE /api/cart/<id>` - 删除购物车商品
8. `POST /api/orders` - 创建订单
9. `GET /api/orders` - 获取订单列表
10. `GET /api/health` - 健康检查

## 项目结构

```
ecommerce-project/
├── backend/                 # Flask后端
│   ├── app.py              # 主应用入口
│   ├── models.py           # 数据库模型
│   ├── config.py           # 配置文件
│   ├── seed_data.py        # 种子数据
│   └── requirements.txt    # Python依赖
├── frontend/               # Next.js前端
│   ├── app/               # 页面路由
│   │   ├── page.tsx       # 首页
│   │   ├── product/[id]/  # 商品详情
│   │   ├── cart/          # 购物车
│   │   └── orders/        # 订单页
│   ├── components/        # 组件
│   │   └── Header.tsx     # 导航头
│   ├── lib/               # 工具库
│   │   └── api.ts         # API封装
│   ├── package.json
│   └── next.config.js
├── docs/                   # 文档
│   ├── API.md             # API文档
│   └── prompt_log.md      # Prompt日志
└── README.md
```

## 本地开发

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端服务将在 `http://localhost:5000` 启动。

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:3000` 启动。

### 3. 访问应用

打开浏览器访问 `http://localhost:3000`。

## 部署说明

### 后端部署

后端使用 Flask 开发，可部署到任意支持 Python 的云平台：
- Render
- Railway
- PythonAnywhere
- 阿里云/腾讯云云函数

部署时需要设置环境变量：
```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///ecommerce.db
```

### 前端部署

前端使用 Next.js 构建，可部署到：
- Vercel（推荐）
- Netlify
- GitHub Pages

构建命令：
```bash
cd frontend
npm run build
```

## API文档

详见 [docs/API.md](./docs/API.md)

## Prompt日志

详见 [docs/prompt_log.md](./docs/prompt_log.md)

## 作者

AI辅助编程与工程化实训项目
