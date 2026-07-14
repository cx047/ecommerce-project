'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Header from '@/components/Header';
import { getOrders } from '@/lib/api';

interface OrderItem {
  id: number;
  product_id: number;
  quantity: number;
  price_at_time: number;
  product: {
    id: number;
    name: string;
    image_url: string;
  };
}

interface Order {
  id: number;
  total_amount: number;
  status: string;
  customer_name: string;
  customer_email: string;
  created_at: string;
  items: OrderItem[];
}

const statusLabels: Record<string, { text: string; color: string; bg: string }> = {
  pending: { text: '待处理', color: '#92400e', bg: '#fef3c7' },
  completed: { text: '已完成', color: '#065f46', bg: '#d1fae5' },
  cancelled: { text: '已取消', color: '#991b1b', bg: '#fee2e2' },
};

export default function Orders() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadOrders();
  }, []);

  async function loadOrders() {
    setLoading(true);
    try {
      const result = await getOrders();
      setOrders(result.data || []);
    } catch {
      alert('加载订单失败');
    } finally {
      setLoading(false);
    }
  }

  function formatDate(dateString: string) {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  return (
    <>
      <Header />
      <main className="container" style={{ padding: '40px 20px', minHeight: '60vh' }}>
        <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '24px' }}>
          我的订单
        </h1>

        {loading ? (
          <div className="loading">加载中...</div>
        ) : orders.length === 0 ? (
          <div className="empty">
            <div className="empty-icon">📋</div>
            <p style={{ fontSize: '18px', marginBottom: '16px' }}>暂无订单</p>
            <Link href="/" className="btn btn-primary">
              去购物
            </Link>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {orders.map((order) => {
              const status = statusLabels[order.status] || statusLabels.pending;
              return (
                <div
                  key={order.id}
                  style={{
                    backgroundColor: 'white',
                    borderRadius: '12px',
                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                    overflow: 'hidden',
                  }}
                >
                  {/* Order Header */}
                  <div
                    style={{
                      padding: '20px',
                      borderBottom: '1px solid #e5e7eb',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      flexWrap: 'wrap',
                      gap: '12px',
                    }}
                  >
                    <div>
                      <span style={{ fontSize: '14px', color: '#6b7280' }}>
                        订单号：#{order.id}
                      </span>
                      <span
                        style={{
                          marginLeft: '16px',
                          padding: '4px 12px',
                          borderRadius: '20px',
                          fontSize: '12px',
                          fontWeight: '600',
                          backgroundColor: status.bg,
                          color: status.color,
                        }}
                      >
                        {status.text}
                      </span>
                    </div>
                    <span style={{ fontSize: '14px', color: '#6b7280' }}>
                      {formatDate(order.created_at)}
                    </span>
                  </div>

                  {/* Order Items */}
                  <div style={{ padding: '20px' }}>
                    {order.items.map((item) => (
                      <div
                        key={item.id}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '16px',
                          padding: '12px 0',
                          borderBottom: '1px solid #f3f4f6',
                        }}
                      >
                        <img
                          src={item.product.image_url}
                          alt={item.product.name}
                          style={{
                            width: '60px',
                            height: '60px',
                            objectFit: 'cover',
                            borderRadius: '8px',
                          }}
                        />
                        <div style={{ flex: 1 }}>
                          <p style={{ fontWeight: '500', marginBottom: '4px' }}>
                            {item.product.name}
                          </p>
                          <p style={{ fontSize: '14px', color: '#6b7280' }}>
                            ¥{item.price_at_time.toFixed(2)} x {item.quantity}
                          </p>
                        </div>
                        <p style={{ fontWeight: 'bold', color: '#2563eb' }}>
                          ¥{(item.price_at_time * item.quantity).toFixed(2)}
                        </p>
                      </div>
                    ))}
                  </div>

                  {/* Order Footer */}
                  <div
                    style={{
                      padding: '20px',
                      backgroundColor: '#f9fafb',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      flexWrap: 'wrap',
                      gap: '12px',
                    }}
                  >
                    <div>
                      <p style={{ fontSize: '14px', color: '#6b7280' }}>
                        收货人：{order.customer_name || '匿名用户'}
                      </p>
                      {order.customer_email && (
                        <p style={{ fontSize: '14px', color: '#6b7280' }}>
                          邮箱：{order.customer_email}
                        </p>
                      )}
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <span style={{ fontSize: '14px', color: '#6b7280' }}>订单金额：</span>
                      <span style={{ fontSize: '24px', fontWeight: 'bold', color: '#2563eb' }}>
                        ¥{order.total_amount.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
    </>
  );
}
