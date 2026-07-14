'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Header from '@/components/Header';
import { getCart, updateCartItem, removeFromCart, clearCart, createOrder } from '@/lib/api';

interface CartItem {
  id: number;
  product_id: number;
  quantity: number;
  product: {
    id: number;
    name: string;
    price: number;
    image_url: string;
    stock: number;
  };
}

export default function Cart() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [checkoutLoading, setCheckoutLoading] = useState(false);
  const [customerName, setCustomerName] = useState('');
  const [customerEmail, setCustomerEmail] = useState('');
  const [showCheckout, setShowCheckout] = useState(false);

  useEffect(() => {
    loadCart();
  }, []);

  async function loadCart() {
    setLoading(true);
    try {
      const result = await getCart();
      setCartItems(result.data || []);
      setTotal(result.total || 0);
    } catch {
      alert('加载购物车失败');
    } finally {
      setLoading(false);
    }
  }

  async function handleUpdateQuantity(itemId: number, quantity: number) {
    try {
      await updateCartItem(itemId, quantity);
      await loadCart();
      window.dispatchEvent(new Event('cartUpdated'));
    } catch (err: any) {
      alert(err.message || '更新失败');
    }
  }

  async function handleRemove(itemId: number) {
    if (!confirm('确定要移除这个商品吗？')) return;
    try {
      await removeFromCart(itemId);
      await loadCart();
      window.dispatchEvent(new Event('cartUpdated'));
    } catch {
      alert('移除失败');
    }
  }

  async function handleClear() {
    if (!confirm('确定要清空购物车吗？')) return;
    try {
      await clearCart();
      await loadCart();
      window.dispatchEvent(new Event('cartUpdated'));
    } catch {
      alert('清空失败');
    }
  }

  async function handleCheckout() {
    if (!customerName.trim()) {
      alert('请输入您的姓名');
      return;
    }
    
    setCheckoutLoading(true);
    try {
      await createOrder(customerName, customerEmail);
      alert('订单提交成功！');
      setShowCheckout(false);
      await loadCart();
      window.dispatchEvent(new Event('cartUpdated'));
    } catch (err: any) {
      alert(err.message || '下单失败');
    } finally {
      setCheckoutLoading(false);
    }
  }

  return (
    <>
      <Header />
      <main className="container" style={{ padding: '40px 20px', minHeight: '60vh' }}>
        <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '24px' }}>
          购物车
        </h1>

        {loading ? (
          <div className="loading">加载中...</div>
        ) : cartItems.length === 0 ? (
          <div className="empty">
            <div className="empty-icon">🛒</div>
            <p style={{ fontSize: '18px', marginBottom: '16px' }}>购物车是空的</p>
            <Link href="/" className="btn btn-primary">
              去逛逛
            </Link>
          </div>
        ) : (
          <>
            <div style={{ marginBottom: '16px', textAlign: 'right' }}>
              <button onClick={handleClear} className="btn btn-danger" style={{ fontSize: '14px', padding: '8px 16px' }}>
                清空购物车
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {cartItems.map((item) => (
                <div
                  key={item.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '20px',
                    backgroundColor: 'white',
                    padding: '20px',
                    borderRadius: '12px',
                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                  }}
                >
                  <img
                    src={item.product.image_url}
                    alt={item.product.name}
                    style={{
                      width: '100px',
                      height: '100px',
                      objectFit: 'cover',
                      borderRadius: '8px',
                    }}
                  />
                  <div style={{ flex: 1 }}>
                    <Link href={`/product/${item.product.id}`}>
                      <h3 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '8px' }}>
                        {item.product.name}
                      </h3>
                    </Link>
                    <p style={{ fontSize: '16px', color: '#2563eb', fontWeight: 'bold' }}>
                      ¥{item.product.price.toFixed(2)}
                    </p>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                      style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '6px',
                        border: '1px solid #d1d5db',
                        backgroundColor: 'white',
                        cursor: 'pointer',
                      }}
                    >
                      -
                    </button>
                    <span style={{ minWidth: '40px', textAlign: 'center', fontWeight: 'bold' }}>
                      {item.quantity}
                    </span>
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                      style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '6px',
                        border: '1px solid #d1d5db',
                        backgroundColor: 'white',
                        cursor: 'pointer',
                      }}
                    >
                      +
                    </button>
                  </div>
                  <div style={{ minWidth: '100px', textAlign: 'right' }}>
                    <p style={{ fontSize: '18px', fontWeight: 'bold', color: '#2563eb' }}>
                      ¥{(item.product.price * item.quantity).toFixed(2)}
                    </p>
                  </div>
                  <button
                    onClick={() => handleRemove(item.id)}
                    style={{
                      backgroundColor: 'transparent',
                      border: 'none',
                      color: '#ef4444',
                      cursor: 'pointer',
                      fontSize: '20px',
                      padding: '8px',
                    }}
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>

            {/* Cart Summary */}
            <div style={{
              marginTop: '32px',
              backgroundColor: 'white',
              padding: '24px',
              borderRadius: '12px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '24px',
              }}>
                <span style={{ fontSize: '18px' }}>合计：</span>
                <span style={{ fontSize: '28px', fontWeight: 'bold', color: '#2563eb' }}>
                  ¥{total.toFixed(2)}
                </span>
              </div>

              {!showCheckout ? (
                <button
                  onClick={() => setShowCheckout(true)}
                  className="btn btn-primary"
                  style={{ width: '100%', padding: '16px', fontSize: '18px' }}
                >
                  立即结算
                </button>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <input
                    type="text"
                    placeholder="您的姓名 *"
                    value={customerName}
                    onChange={(e) => setCustomerName(e.target.value)}
                    style={{
                      padding: '12px 16px',
                      borderRadius: '8px',
                      border: '1px solid #d1d5db',
                      fontSize: '16px',
                    }}
                  />
                  <input
                    type="email"
                    placeholder="邮箱（可选）"
                    value={customerEmail}
                    onChange={(e) => setCustomerEmail(e.target.value)}
                    style={{
                      padding: '12px 16px',
                      borderRadius: '8px',
                      border: '1px solid #d1d5db',
                      fontSize: '16px',
                    }}
                  />
                  <div style={{ display: 'flex', gap: '16px' }}>
                    <button
                      onClick={() => setShowCheckout(false)}
                      className="btn btn-secondary"
                      style={{ flex: 1, padding: '14px' }}
                    >
                      取消
                    </button>
                    <button
                      onClick={handleCheckout}
                      disabled={checkoutLoading}
                      className="btn btn-primary"
                      style={{ flex: 1, padding: '14px' }}
                    >
                      {checkoutLoading ? '提交中...' : '确认下单'}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </>
        )}
      </main>
    </>
  );
}
