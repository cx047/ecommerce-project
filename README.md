# 优选商城 - AI辅助编程与工程化实训项目

一个全栈电商应用，包含商品展示、购物车、规格选择、虚拟支付、订单管理等完整功能。

## 线上访问地址

**https://ecommerce-project-production-167a.up.railway.app**

## 技术栈

- **后端**: Python 3.11 + Flask 3.0 + Flask-SQLAlchemy + Flask-CORS
- **前端**: 原生 HTML + CSS + JavaScript (SPA 单页应用，Hash 路由)
- **数据库**: SQLite
- **部署**: Railway (Nixpacks 自动构建)
- **版本控制**: Git + GitHub

## 功能特性

### 前端页面（7个独立路由）
1. **首页** (`#/`) - Hero Banner、搜索栏、分类筛选（7个分类）、商品网格展示
2. **商品详情** (`#/product/:id`) - 商品信息、规格选择器、数量选择、加入购物车
3. **购物车** (`#/cart`) - 商品列表、规格详情显示、数量加减、小计/总价、清空/结算
4. **订单页** (`#/orders`) - 历史订单列表、订单状态标签、商品规格详情
5. **个人中心** (`#/profile`) - 头像昵称、订单统计、累计消费、个人信息编辑
6. **支付页** (`#/payment`) - 支付方式选择弹窗（支付宝/微信/银行卡）
7. **支付结果** (`#/payresult`) - 支付成功/失败反馈页面

### 商品分类（7个）
数码电子、服饰穿搭、家居生活、美妆个护、运动户外、食品生鲜、图书文创

### 商品规格系统
- 每个商品可配置多个规格维度（颜色、尺码、版本等）
- 同一商品不同规格可同时存在于购物车
- 购物车和订单均显示所选规格详情

### 后端API（12个接口）
1. `GET /api/products` - 商品列表（支持分类筛选、搜索）
2. `GET /api/products/<id>` - 商品详情
3. `GET /api/products/categories` - 商品分类列表
4. `GET /api/cart` - 获取购物车
5. `POST /api/cart` - 添加到购物车（含规格选择）
6. `PUT /api/cart/<id>` - 更新购物车数量
7. `DELETE /api/cart/<id>` - 删除购物车项
8. `DELETE /api/cart/clear` - 清空购物车
9. `GET /api/orders` - 获取订单列表
10. `POST /api/orders` - 创建订单
11. `GET /api/orders/<id>` - 获取订单详情
12. `GET /api/health` - 健康检查

## 项目结构

```
ecommerce-project/
├── backend/                  # Flask 后端 + 静态前端
│   ├── app.py               # 主应用入口、API路由
│   ├── models.py            # 数据库模型（Product/CartItem/Order/OrderItem）
│   ├── config.py            # 配置文件
│   ├── seed_data.py         # 种子数据（21个商品、7个分类）
│   ├── requirements.txt     # Python 依赖
│   ├── static/              # 静态资源
│   │   ├── index.html       # SPA 单页应用（所有前端代码）
│   │   └── images/          # 商品图片（20张AI生成）
│   └── tests/               # 单元测试
│       └── test_api.py      # API 接口测试
├── docs/                    # 项目文档
│   ├── API.md              # API 接口文档
│   ├── prompt_log.md       # AI Prompt 交互日志
│   ├── code_review.md      # AI 代码审查报告
│   └── personal_summary.md # 个人实训总结
├── frontend/                # 原始 Next.js 前端（已废弃，保留作参考）
├── screenshots/             # 接口测试截图
├── .gitignore
└── README.md
```

## 本地开发

### 1. 环境要求
- Python 3.11+
- pip

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端服务将在 `http://localhost:5000` 启动，前端页面访问 `http://localhost:5000/`。

### 3. 运行测试

```bash
cd backend
pip install pytest
pytest tests/ -v
```

## 部署说明

项目部署在 Railway 平台，使用 Nixpacks 自动构建：
- 检测到 `requirements.txt` 自动安装 Python 依赖
- 启动命令：`python backend/app.py`
- 绑定 PORT 环境变量
- 数据库使用 SQLite 文件存储

## Git 提交规范

项目使用 Conventional Commits 规范：
- `feat:` 新功能
- `fix:` 修复Bug
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

## 作者

AI辅助编程与工程化实训项目
