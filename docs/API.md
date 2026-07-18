# API 接口文档

## 基础信息

- **生产环境 Base URL**: `https://ecommerce-project-production-167a.up.railway.app/api`
- **本地开发 Base URL**: `http://localhost:5000/api`
- **Content-Type**: `application/json`
- **会话标识**: 所有请求需携带请求头 `X-Session-ID`，值为 UUID 格式，用于标识用户会话

### 请求头

| 头部 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Content-Type | string | 是 | 固定值 `application/json` |
| X-Session-ID | string | 是 | 用户会话标识（UUID 格式），如 `550e8400-e29b-41d4-a716-446655440000` |

### 统一响应格式

```json
{
  "success": true,
  "data": "...",
  "error": "..."
}
```

- `success` (boolean): 请求是否成功
- `data`: 成功时返回的数据
- `error` (string): 失败时的错误描述

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 一、商品接口

### 1. 获取商品列表

```
GET /api/products
```

获取所有商品，支持按分类筛选和按名称搜索。

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category | string | 否 | 按分类筛选，可选值：`electronics`、`clothing`、`home`、`beauty`、`sports`、`food`、`books` |
| search | string | 否 | 按商品名称模糊搜索 |

**响应示例**:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "无线蓝牙耳机 Pro",
      "description": "高音质降噪无线蓝牙耳机，支持主动降噪，续航30小时，IPX7防水等级。采用最新蓝牙5.3技术，连接稳定低延迟。",
      "price": 299.0,
      "image_url": "/images/headphones.jpg",
      "category": "electronics",
      "stock": 50,
      "specifications": [
        {
          "name": "颜色",
          "options": ["曜石黑", "象牙白", "天空蓝"]
        },
        {
          "name": "版本",
          "options": ["标准版", "降噪版"]
        }
      ],
      "created_at": "2026-07-15T09:25:25.746386"
    },
    {
      "id": 2,
      "name": "智能运动手表",
      "description": "多功能智能手表，支持心率监测、血氧检测、GPS定位。50米防水，7天超长续航，100+运动模式。",
      "price": 599.0,
      "image_url": "/images/watch.jpg",
      "category": "electronics",
      "stock": 30,
      "specifications": [
        {
          "name": "颜色",
          "options": ["深空灰", "星光银", "玫瑰金"]
        },
        {
          "name": "表带",
          "options": ["硅胶", "金属", "真皮"]
        }
      ],
      "created_at": "2026-07-15T09:25:25.746386"
    }
  ],
  "count": 2
}
```

---

### 2. 获取商品详情

```
GET /api/products/<id>
```

根据商品 ID 获取单个商品的详细信息。

**路径参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 商品 ID |

**响应示例**:

```json
{
  "success": true,
  "data": {
    "id": 3,
    "name": "极简纯棉T恤",
    "description": "100%新疆长绒棉，亲肤透气。经典版型设计，多色可选。经过预缩水处理，不易变形。",
    "price": 89.0,
    "image_url": "/images/tshirt.jpg",
    "category": "clothing",
    "stock": 200,
    "specifications": [
      {
        "name": "颜色",
        "options": ["白色", "黑色", "灰色", "藏青"]
      },
      {
        "name": "尺码",
        "options": ["S", "M", "L", "XL", "XXL"]
      }
    ],
    "created_at": "2026-07-15T09:25:25.746386"
  }
}
```

**错误响应**（商品不存在）:

```json
{
  "success": false,
  "error": "Resource not found"
}
```

---

### 3. 获取商品分类列表

```
GET /api/products/categories
```

获取所有已有的商品分类。

**响应示例**:

```json
{
  "success": true,
  "data": [
    "electronics",
    "clothing",
    "home",
    "beauty",
    "sports",
    "food",
    "books"
  ]
}
```

> **说明**: 返回数据库中所有已存在的分类标识。完整分类列表如下：
>
> | 标识 | 中文名称 |
> |------|----------|
> | electronics | 数码电子 |
> | clothing | 服饰穿搭 |
> | home | 家居生活 |
> | beauty | 美妆个护 |
> | sports | 运动户外 |
> | food | 食品生鲜 |
> | books | 图书文创 |

---

## 二、购物车接口

### 4. 获取购物车

```
GET /api/cart
```

获取当前会话购物车中的所有商品。

**请求头**:

| 头部 | 说明 |
|------|------|
| X-Session-ID | 用户会话标识 |

**响应示例**:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "product_id": 3,
      "quantity": 2,
      "selected_specs": {
        "颜色": "白色",
        "尺码": "L"
      },
      "spec_details": "颜色: 白色, 尺码: L",
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "product": {
        "id": 3,
        "name": "极简纯棉T恤",
        "description": "100%新疆长绒棉，亲肤透气。经典版型设计，多色可选。经过预缩水处理，不易变形。",
        "price": 89.0,
        "image_url": "/images/tshirt.jpg",
        "category": "clothing",
        "stock": 200,
        "specifications": [
          {
            "name": "颜色",
            "options": ["白色", "黑色", "灰色", "藏青"]
          },
          {
            "name": "尺码",
            "options": ["S", "M", "L", "XL", "XXL"]
          }
        ],
        "created_at": "2026-07-15T09:25:25.746386"
      },
      "created_at": "2026-07-15T10:00:00.000000"
    },
    {
      "id": 2,
      "product_id": 3,
      "quantity": 1,
      "selected_specs": {
        "颜色": "黑色",
        "尺码": "M"
      },
      "spec_details": "颜色: 黑色, 尺码: M",
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "product": {
        "id": 3,
        "name": "极简纯棉T恤",
        "description": "100%新疆长绒棉，亲肤透气。经典版型设计，多色可选。经过预缩水处理，不易变形。",
        "price": 89.0,
        "image_url": "/images/tshirt.jpg",
        "category": "clothing",
        "stock": 200,
        "specifications": [
          {
            "name": "颜色",
            "options": ["白色", "黑色", "灰色", "藏青"]
          },
          {
            "name": "尺码",
            "options": ["S", "M", "L", "XL", "XXL"]
          }
        ],
        "created_at": "2026-07-15T09:25:25.746386"
      },
      "created_at": "2026-07-15T10:05:00.000000"
    }
  ],
  "total": 267.0,
  "count": 2,
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

> **说明**: 同一商品的不同规格会作为独立的购物车项存在。`total` 为所有商品的 `price * quantity` 之和。`spec_details` 是 `selected_specs` 的可读文本格式。

---

### 5. 添加商品到购物车

```
POST /api/cart
```

将商品添加到购物车。如果同一商品、同一规格已存在于购物车中，则数量累加。

**请求头**:

| 头部 | 说明 |
|------|------|
| X-Session-ID | 用户会话标识 |
| Content-Type | application/json |

**请求体参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| product_id | integer | 是 | 商品 ID |
| quantity | integer | 否 | 数量，默认为 1 |
| selected_specs | object | 否 | 已选规格键值对，如 `{"颜色": "红色", "尺码": "M"}` |

**请求示例**:

```json
{
  "product_id": 3,
  "quantity": 2,
  "selected_specs": {
    "颜色": "白色",
    "尺码": "L"
  }
}
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "product_id": 3,
    "quantity": 2,
    "selected_specs": {
      "颜色": "白色",
      "尺码": "L"
    },
    "spec_details": "颜色: 白色, 尺码: L",
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "product": {
      "id": 3,
      "name": "极简纯棉T恤",
      "description": "100%新疆长绒棉，亲肤透气。经典版型设计，多色可选。经过预缩水处理，不易变形。",
      "price": 89.0,
      "image_url": "/images/tshirt.jpg",
      "category": "clothing",
      "stock": 200,
      "specifications": [
        {
          "name": "颜色",
          "options": ["白色", "黑色", "灰色", "藏青"]
        },
        {
          "name": "尺码",
          "options": ["S", "M", "L", "XL", "XXL"]
        }
      ],
      "created_at": "2026-07-15T09:25:25.746386"
    },
    "created_at": "2026-07-15T10:00:00.000000"
  },
  "message": "Item added to cart"
}
```

**错误响应**（缺少 product_id）:

```json
{
  "success": false,
  "error": "Product ID is required"
}
```

**错误响应**（库存不足）:

```json
{
  "success": false,
  "error": "Not enough stock. Available: 10"
}
```

---

### 6. 更新购物车商品数量

```
PUT /api/cart/<id>
```

更新购物车中某项商品的数量。当 quantity <= 0 时，会自动删除该商品。

**路径参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 购物车项 ID |

**请求体参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| quantity | integer | 否 | 新的数量，默认为 1；若 <= 0 则删除该购物车项 |

**请求示例**:

```json
{
  "quantity": 3
}
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "product_id": 3,
    "quantity": 3,
    "selected_specs": {
      "颜色": "白色",
      "尺码": "L"
    },
    "spec_details": "颜色: 白色, 尺码: L",
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "product": {
      "id": 3,
      "name": "极简纯棉T恤",
      "description": "100%新疆长绒棉，亲肤透气。",
      "price": 89.0,
      "image_url": "/images/tshirt.jpg",
      "category": "clothing",
      "stock": 200,
      "specifications": [
        {"name": "颜色", "options": ["白色", "黑色", "灰色", "藏青"]},
        {"name": "尺码", "options": ["S", "M", "L", "XL", "XXL"]}
      ],
      "created_at": "2026-07-15T09:25:25.746386"
    },
    "created_at": "2026-07-15T10:00:00.000000"
  },
  "message": "Cart updated"
}
```

**响应示例**（quantity <= 0，删除成功）:

```json
{
  "success": true,
  "message": "Item removed from cart"
}
```

---

### 7. 删除购物车商品

```
DELETE /api/cart/<id>
```

从购物车中删除指定商品项。

**路径参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 购物车项 ID |

**响应示例**:

```json
{
  "success": true,
  "message": "Item removed from cart"
}
```

---

### 8. 清空购物车

```
DELETE /api/cart/clear
```

清空当前会话的所有购物车商品。

**响应示例**:

```json
{
  "success": true,
  "message": "Cart cleared"
}
```

---

## 三、订单接口

### 9. 获取订单列表

```
GET /api/orders
```

获取当前会话的所有订单，按创建时间倒序排列。

**请求头**:

| 头部 | 说明 |
|------|------|
| X-Session-ID | 用户会话标识 |

**响应示例**:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "total_amount": 357.0,
      "status": "completed",
      "customer_name": "张三",
      "customer_email": "zhangsan@example.com",
      "items": [
        {
          "id": 1,
          "order_id": 1,
          "product_id": 1,
          "quantity": 1,
          "price_at_time": 299.0,
          "selected_specs": {
            "颜色": "曜石黑",
            "版本": "降噪版"
          },
          "spec_details": "颜色: 曜石黑, 版本: 降噪版",
          "product": {
            "id": 1,
            "name": "无线蓝牙耳机 Pro",
            "description": "高音质降噪无线蓝牙耳机，支持主动降噪，续航30小时，IPX7防水等级。",
            "price": 299.0,
            "image_url": "/images/headphones.jpg",
            "category": "electronics",
            "stock": 49,
            "specifications": [
              {"name": "颜色", "options": ["曜石黑", "象牙白", "天空蓝"]},
              {"name": "版本", "options": ["标准版", "降噪版"]}
            ],
            "created_at": "2026-07-15T09:25:25.746386"
          }
        }
      ],
      "created_at": "2026-07-15T10:30:00.000000"
    }
  ],
  "count": 1
}
```

---

### 10. 创建订单

```
POST /api/orders
```

将购物车中的所有商品结算生成订单。创建成功后会自动清空购物车，并扣减对应商品库存。

**请求头**:

| 头部 | 说明 |
|------|------|
| X-Session-ID | 用户会话标识 |
| Content-Type | application/json |

**请求体参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| customer_name | string | 否 | 顾客姓名 |
| customer_email | string | 否 | 顾客邮箱 |

**请求示例**:

```json
{
  "customer_name": "张三",
  "customer_email": "zhangsan@example.com"
}
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "total_amount": 357.0,
    "status": "completed",
    "customer_name": "张三",
    "customer_email": "zhangsan@example.com",
    "items": [
      {
        "id": 1,
        "order_id": 1,
        "product_id": 1,
        "quantity": 1,
        "price_at_time": 299.0,
        "selected_specs": {
          "颜色": "曜石黑",
          "版本": "降噪版"
        },
        "spec_details": "颜色: 曜石黑, 版本: 降噪版",
        "product": {
          "id": 1,
          "name": "无线蓝牙耳机 Pro",
          "description": "高音质降噪无线蓝牙耳机，支持主动降噪，续航30小时，IPX7防水等级。",
          "price": 299.0,
          "image_url": "/images/headphones.jpg",
          "category": "electronics",
          "stock": 49,
          "specifications": [
            {"name": "颜色", "options": ["曜石黑", "象牙白", "天空蓝"]},
            {"name": "版本", "options": ["标准版", "降噪版"]}
          ],
          "created_at": "2026-07-15T09:25:25.746386"
        }
      },
      {
        "id": 2,
        "order_id": 1,
        "product_id": 17,
        "quantity": 2,
        "price_at_time": 29.0,
        "selected_specs": {
          "产地": "耶加雪菲",
          "烘焙度": "中烘"
        },
        "spec_details": "产地: 耶加雪菲, 烘焙度: 中烘",
        "product": {
          "id": 17,
          "name": "精品手冲咖啡豆",
          "description": "埃塞俄比亚耶加雪菲，水洗处理。",
          "price": 88.0,
          "image_url": "/images/coffeebeans.jpg",
          "category": "food",
          "stock": 88,
          "specifications": [
            {"name": "产地", "options": ["耶加雪菲", "哥伦比亚", "曼特宁"]},
            {"name": "烘焙度", "options": ["浅烘", "中烘", "深烘"]},
            {"name": "规格", "options": ["250g", "500g", "1kg"]}
          ],
          "created_at": "2026-07-15T09:25:25.746386"
        }
      }
    ],
    "created_at": "2026-07-15T10:30:00.000000"
  },
  "message": "Order created successfully"
}
```

> **说明**:
> - `total_amount` 为所有购物车商品的 `price * quantity` 之和
> - `price_at_time` 记录下单时的商品单价，不受后续价格变动影响
> - 每个订单项保留 `selected_specs`（规格键值对）和 `spec_details`（可读规格文本）
> - 订单创建后购物车自动清空，商品库存相应扣减

**错误响应**（购物车为空）:

```json
{
  "success": false,
  "error": "Cart is empty"
}
```

---

### 11. 获取订单详情

```
GET /api/orders/<id>
```

根据订单 ID 获取订单详情（仅限当前会话）。

**路径参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 订单 ID |

**响应示例**:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "total_amount": 357.0,
    "status": "completed",
    "customer_name": "张三",
    "customer_email": "zhangsan@example.com",
    "items": [
      {
        "id": 1,
        "order_id": 1,
        "product_id": 1,
        "quantity": 1,
        "price_at_time": 299.0,
        "selected_specs": {
          "颜色": "曜石黑",
          "版本": "降噪版"
        },
        "spec_details": "颜色: 曜石黑, 版本: 降噪版",
        "product": {
          "id": 1,
          "name": "无线蓝牙耳机 Pro",
          "description": "高音质降噪无线蓝牙耳机，支持主动降噪，续航30小时，IPX7防水等级。",
          "price": 299.0,
          "image_url": "/images/headphones.jpg",
          "category": "electronics",
          "stock": 49,
          "specifications": [
            {"name": "颜色", "options": ["曜石黑", "象牙白", "天空蓝"]},
            {"name": "版本", "options": ["标准版", "降噪版"]}
          ],
          "created_at": "2026-07-15T09:25:25.746386"
        }
      }
    ],
    "created_at": "2026-07-15T10:30:00.000000"
  }
}
```

---

## 四、健康检查接口

### 12. 服务健康检查

```
GET /api/health
```

检查 API 服务是否正常运行。此接口不需要 `X-Session-ID` 请求头。

**响应示例**:

```json
{
  "status": "healthy",
  "service": "ecommerce-api",
  "version": "1.0.0"
}
```

---

## 附录：数据模型说明

### Product（商品）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 商品 ID（主键） |
| name | string | 商品名称 |
| description | string | 商品描述 |
| price | float | 商品价格 |
| image_url | string | 商品图片路径 |
| category | string | 商品分类标识 |
| stock | integer | 库存数量 |
| specifications | array | 规格配置，格式：`[{"name": "颜色", "options": ["红", "黑"]}]` |
| created_at | datetime | 创建时间 |

### CartItem（购物车项）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 购物车项 ID（主键） |
| product_id | integer | 关联商品 ID |
| quantity | integer | 数量 |
| selected_specs | object | 已选规格，格式：`{"颜色": "红", "尺码": "M"}` |
| session_id | string | 用户会话 ID |
| created_at | datetime | 创建时间 |
| product | object | 关联的商品详情（嵌套对象） |
| spec_details | string | 规格可读文本，如 `"颜色: 红, 尺码: M"` |

### Order（订单）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 订单 ID（主键） |
| session_id | string | 用户会话 ID |
| total_amount | float | 订单总金额 |
| status | string | 订单状态（如 `completed`） |
| customer_name | string | 顾客姓名 |
| customer_email | string | 顾客邮箱 |
| items | array | 订单项列表（嵌套对象） |
| created_at | datetime | 创建时间 |

### OrderItem（订单项）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 订单项 ID（主键） |
| order_id | integer | 关联订单 ID |
| product_id | integer | 关联商品 ID |
| quantity | integer | 数量 |
| price_at_time | float | 下单时商品单价 |
| selected_specs | object | 已选规格（与购物车一致） |
| spec_details | string | 规格可读文本 |
| product | object | 关联的商品详情（嵌套对象） |
