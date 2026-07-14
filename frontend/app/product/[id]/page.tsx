'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import Header from '@/components/Header';
import { getProduct, addToCart } from '@/lib/api';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  image_url: string;
  category: string;
  stock: number;
  created_at: string;
}

const categoryLabels: Record<string, string> = {
  electronics: '数码电子',
  clothing: '服饰穿搭',
  home: '家居生活',
};

export default function ProductDetail() {
  const params = useParams();
  const productId = Number(params.id);
  
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [addingToCart, setAddingToCart] = useState(false);

  useEffect(() => {
    if (productId) {
      loadProduct();
    }
  }, [productId]);

  async function loadProduct() {
    setLoading(true);
    try {
      const result = await getProduct(productId);
      setProduct(result.data);
      setError('');
    } catch {
      setError('加载商品详情失败');
    } finally {
      setLoading(false);
    }
  }

  async function handleAddToCart() {
    if (!product) return;
    setAddingToCart(true);
    try {
      await addToCart(product.id, quantity);
      window.dispatchEvent(new Event('cartUpdated'));
      alert(`已将 ${quantity} 件商品添加到购物车！`);
    } catch (err: any) {
      alert(err.message || '添加失败');
    } finally {
      setAddingToCart(false);
    }
  }

  if (loading) {
    return (
      <>
        <Header />
        <div className="loading">加载中...</div>
      </>
    );
  }

  if (error || !product) {
    return (
      <>
        <Header />
        <div className="error">
          <p>{error || '商品不存在'}</p>
          <Link href="/" style={{ color: '#2563eb', marginTop: '16px', display: 'inline-block' }}>
            返回首页
          </Link>
        </div>
      </>
    );
  }

  return (
    <>
      <Header />
      <main className="container" style={{ padding: '40px 20px' }}>
        {/* Breadcrumb */}
        <nav style={{ marginBottom: '24px', fontSize: '14px', color: '#6b7280' }}>
          <Link href="/" style={{ color: '#2563eb' }}>首页</Link>
          <span style={{ margin: '0 8px' }}>/</span>
          <span>{product.name}</span>
        </nav>

        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '48px',
          backgroundColor: 'white',
          borderRadius: '12px',
          padding: '40px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        }}>
          {/* Product Image */}
          <div style={{
            borderRadius: '12px',
            overflow: 'hidden',
            backgroundColor: '#f3f4f6',
          }}>
            <img
              src={product.image_url}
              alt={product.name}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
              }}
            />
          </div>

          {/* Product Info */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <span className="badge badge-blue">
              {categoryLabels[product.category] || product.category}
            </span>
            
            <h1 style={{ fontSize: '32px', fontWeight: 'bold', color: '#111827' }}>
              {product.name}
            </h1>
            
            <p style={{ fontSize: '16px', color: '#6b7280', lineHeight: 1.6 }}>
              {product.description}
            </p>
            
            <div style={{
              padding: '20px',
              backgroundColor: '#f9fafb',
              borderRadius: '8px',
            }}>
              <div style={{ fontSize: '14px', color: '#6b7280', marginBottom: '8px' }}>
                售价
              </div>
              <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#2563eb' }}>
                ¥{product.price.toFixed(2)}
              </div>
            </div>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <span style={{ fontSize: '14px', color: '#6b7280' }}>数量：</span>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  style={{
                    width: '36px',
                    height: '36px',
                    borderRadius: '8px',
                    border: '1px solid #d1d5db',
                    backgroundColor: 'white',
                    cursor: 'pointer',
                    fontSize: '18px',
                  }}
                >
                  -
                </button>
                <span style={{ fontSize: '18px', fontWeight: 'bold', minWidth: '40px', textAlign: 'center' }}>
                  {quantity}
                </span>
                <button
                  onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                  style={{
                    width: '36px',
                    height: '36px',
                    borderRadius: '8px',
                    border: '1px solid #d1d5db',
                    backgroundColor: 'white',
                    cursor: 'pointer',
                    fontSize: '18px',
                  }}
                >
                  +
                </button>
              </div>
              <span style={{ fontSize: '14px', color: '#6b7280' }}>
                库存：{product.stock} 件
              </span>
            </div>
            
            <div style={{ display: 'flex', gap: '16px', marginTop: '16px' }}>
              <button
                onClick={handleAddToCart}
                disabled={addingToCart}
                className="btn btn-primary"
                style={{ flex: 1, padding: '16px' }}
              >
                {addingToCart ? '添加中...' : '加入购物车'}
              </button>
              <Link href="/cart" className="btn btn-secondary" style={{ flex: 1, padding: '16px' }}>
                去购物车
              </Link>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
