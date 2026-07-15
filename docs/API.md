# API 接口文档

## 基础信息

- **Base URL**: `http://localhost:5000/api`
- **Content-Type**: `application/json`
- **Session标识**: 通过请求头 `X-Session-ID` 传递用户会话ID

---

## 商品接口

### 1. 获取商品列表

```
GET /products
```

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category | string | 否 | 按分类筛选 |
| search | string | 否 | 按名称搜索 |

**响应示例**:
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "id": 1,
      "name": "无线蓝牙耳机 Pro",
      "description": "高音质降噪无线蓝牙耳机...",
      "price": 299.00,
      "image_url": "https://images.unsplash.com/...",
      "category": "electronics",
      "stock": 50,
      "created_at": "2026-07-15T09:25:25.746386"
    }
  ]
}
```

### 2. 获取商品详情

```
GET /products/{id}
```

**路径参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 商品ID |

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "无线蓝牙耳机 Pro",
    "description": "高音质降噪无线蓝牙耳机...",
    "price": 299.00,
    "image_url": "https://images.unsplash.com/...",
    "category": "electronics",
    "stock": 50,
    "created_at": "2026-07-15T09:25:25.746386"
  }
}
```

### 3. 获取商品分类

```
GET /products/categories
```

**响应示例**:
```json
{
  "success": true,
  "data": ["electronics", "clothing", "home"]
}
```

---

## 购物车接口

### 4. 获取购物车

```
GET /cart
```

**请求头**:
| 头部 | 说明 |
|------|------|
| X-Session-ID | 用户会话标识 |

**响应示例**:
```json
{
  "success": true,
  "count": 2,
  "total": 598.00,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [
    {
      "id": 1,
      "product_id": 1,
      "quantity": 2,
      "product": {
        "id": 1,
        "name": "无线蓝牙耳机 Pro",
        "price": 299.00,
        "image_url": "https://images.unsplash.com/..."
      }
    }
  ]
}
```

### 5. 添加商品到购物车

```
POST /cart
```

**请求体**:
```json
{
  "product_id": 1,
  "quantity": 1
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "Item added to cart",
  "data": {
    "id": 1,
    "product_id": 1,
    "quantity": 1
  }
}
```

### 6. 更新购物车商品数量

```
PUT /cart/{item_id}
```

**请求体**:
```json
{
  "quantity": 3
}
```

**说明**: 当 quantity <= 0 时，会删除该商品。

### 7. 删除购物车商品

```
DELETE /cart/{item_id}
```

### 8. 清空购物车

```
DELETE /cart/clear
```

---

## 订单接口

### 9. 创建订单

```
POST /orders
```

**请求体**:
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
  "message": "Order created successfully",
  "data": {
    "id": 1,
    "total_amount": 598.00,
    "status": "completed",
    "customer_name": "张三",
    "items": [...],
    "created_at": "2026-07-15T10:30:00.000000"
  }
}
```

### 10. 获取订单列表

```
GET /orders
```

**响应示例**:
```json
{
  "success": true,
  "count": 1,
  "data": [
    {
      "id": 1,
      "total_amount": 598.00,
      "status": "completed",
      "customer_name": "张三",
      "items": [...],
      "created_at": "2026-07-15T10:30:00.000000"
    }
  ]
}
```

### 11. 获取订单详情

```
GET /orders/{id}
```

---

## 健康检查

### 12. 服务健康检查

```
GET /health
```

**响应示例**:
```json
{
  "status": "healthy",
  "service": "ecommerce-api",
  "version": "1.0.0"
}
```

---

## 错误响应

所有接口在出错时返回统一的错误格式：

```json
{
  "success": false,
  "error": "错误描述信息"
}
```

**HTTP状态码**:
| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
