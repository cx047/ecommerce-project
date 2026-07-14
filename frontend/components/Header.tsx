'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { getCart } from '@/lib/api';

export default function Header() {
  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
    loadCartCount();
    // Listen for cart updates
    window.addEventListener('cartUpdated', loadCartCount);
    return () => window.removeEventListener('cartUpdated', loadCartCount);
  }, []);

  async function loadCartCount() {
    try {
      const result = await getCart();
      setCartCount(result.count || 0);
    } catch {
      setCartCount(0);
    }
  }

  return (
    <header style={{
      backgroundColor: '#ffffff',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
    }}>
      <div className="container" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: '64px',
      }}>
        <Link href="/" style={{
          fontSize: '24px',
          fontWeight: 'bold',
          color: '#2563eb',
        }}>
          优选商城
        </Link>

        <nav style={{
          display: 'flex',
          gap: '32px',
          alignItems: 'center',
        }}>
          <Link href="/" style={{
            fontSize: '16px',
            color: '#374151',
            fontWeight: 500,
          }}>
            首页
          </Link>
          <Link href="/cart" style={{
            fontSize: '16px',
            color: '#374151',
            fontWeight: 500,
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
          }}>
            购物车
            {cartCount > 0 && (
              <span style={{
                backgroundColor: '#ef4444',
                color: 'white',
                fontSize: '12px',
                padding: '2px 8px',
                borderRadius: '10px',
                fontWeight: 'bold',
              }}>
                {cartCount}
              </span>
            )}
          </Link>
          <Link href="/orders" style={{
            fontSize: '16px',
            color: '#374151',
            fontWeight: 500,
          }}>
            我的订单
          </Link>
        </nav>
      </div>
    </header>
  );
}
