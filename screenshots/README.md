# 截图说明

本文件夹包含项目考核所需的截图。

## 1. 数据库表结构截图

### products 表（商品表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER (PK) | 商品ID |
| name | VARCHAR(200) | 商品名称 |
| description | TEXT | 商品描述 |
| price | FLOAT | 价格 |
| image_url | VARCHAR(500) | 图片地址 |
| category | VARCHAR(100) | 分类 |
| stock | INTEGER | 库存 |
| created_at | DATETIME | 创建时间 |
共 10 条数据。

### cart_items 表（购物车表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER (PK) | 购物车项ID |
| product_id | INTEGER (FK) | 关联商品 |
| quantity | INTEGER | 数量 |
| session_id | VARCHAR(100) | 用户会话ID |
| created_at | DATETIME | 创建时间 |

### orders 表（订单表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER (PK) | 订单ID |
| session_id | VARCHAR(100) | 用户会话ID |
| total_amount | FLOAT | 订单总金额 |
| status | VARCHAR(50) | 订单状态 |
| customer_name | VARCHAR(100) | 客户姓名 |
| customer_email | VARCHAR(100) | 客户邮箱 |
| created_at | DATETIME | 创建时间 |

### order_items 表（订单明细表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER (PK) | 明细ID |
| order_id | INTEGER (FK) | 关联订单 |
| product_id | INTEGER (FK) | 关联商品 |
| quantity | INTEGER | 购买数量 |
| price_at_time | FLOAT | 下单时价格 |

## 2. API 接口测试截图

- `api_products.png` - GET /api/products 返回 10 条商品数据
- `api_cart.png` - GET /api/cart 返回购物车数据

## 3. AI Code Review 截图

详见 `docs/code_review.md` 文档。