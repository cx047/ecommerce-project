'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Header from '@/components/Header';
import { getProducts, getCategories, addToCart } from '@/lib/api';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  image_url: string;
  category: string;
  stock: number;
}

const categoryLabels: Record<string, string> = {
  electronics: '数码电子',
  clothing: '服饰穿搭',
  home: '家居生活',
};

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [addingToCart, setAddingToCart] = useState<number | null>(null);

  useEffect(() => {
    loadCategories();
    loadProducts();
  }, []);

  async function loadCategories() {
    try {
      const result = await getCategories();
      setCategories(result.data || []);
    } catch {
      // ignore
    }
  }

  async function loadProducts(category?: string, search?: string) {
    setLoading(true);
    try {
      const result = await getProducts(category, search);
      setProducts(result.data || []);
      setError('');
    } catch (err) {
      setError('加载商品失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  }

  function handleCategoryClick(category: string) {
    const newCategory = selectedCategory === category ? '' : category;
    setSelectedCategory(newCategory);
    loadProducts(newCategory || undefined, searchQuery || undefined);
  }

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    loadProducts(selectedCategory || undefined, searchQuery || undefined);
  }

  async function handleAddToCart(productId: number) {
    setAddingToCart(productId);
    try {
      await addToCart(productId, 1);
      window.dispatchEvent(new Event('cartUpdated'));
      alert('已添加到购物车！');
    } catch (err: any) {
      alert(err.message || '添加失败');
    } finally {
      setAddingToCart(null);
    }
  }

  return (
    <>
      <Header />
      
      {/* Hero Banner */}
      <div style={{
        background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
        color: 'white',
        padding: '60px 20px',
        textAlign: 'center',
      }}>
        <div className="container">
          <h1 style={{ fontSize: '36px', fontWeight: 'bold', marginBottom: '16px' }}>
            品质生活，优选好物
          </h1>
          <p style={{ fontSize: '18px', opacity: 0.9, marginBottom: '32px' }}>
            精选数码、服饰、家居，为您打造理想生活
          </p>
          
          {/* Search Bar */}
          <form onSubmit={handleSearch} style={{
            display: 'flex',
            maxWidth: '600px',
            margin: '0 auto',
            gap: '12px',
          }}>
            <input
              type="text"
              placeholder="搜索商品..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                flex: 1,
                padding: '14px 20px',
                borderRadius: '8px',
                border: 'none',
                fontSize: '16px',
                outline: 'none',
              }}
            />
            <button type="submit" className="btn btn-primary">
              搜索
            </button>
          </form>
        </div>
      </div>

      <main className="container" style={{ padding: '40px 20px' }}>
        {/* Category Filter */}
        <div style={{
          display: 'flex',
          gap: '12px',
          marginBottom: '32px',
          flexWrap: 'wrap',
        }}>
          <button
            onClick={() => handleCategoryClick('')}
            className={`badge ${selectedCategory === '' ? 'badge-blue' : 'badge-yellow'}`}
            style={{ cursor: 'pointer', fontSize: '14px', padding: '8px 16px' }}
          >
            全部
          </button>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => handleCategoryClick(cat)}
              className={`badge ${selectedCategory === cat ? 'badge-blue' : 'badge-yellow'}`}
              style={{ cursor: 'pointer', fontSize: '14px', padding: '8px 16px' }}
            >
              {categoryLabels[cat] || cat}
            </button>
          ))}
        </div>

        {/* Products Grid */}
        {loading ? (
          <div className="loading">加载中...</div>
        ) : error ? (
          <div className="error">{error}</div>
        ) : products.length === 0 ? (
          <div className="empty">
            <div className="empty-icon">📦</div>
            <p>暂无商品</p>
          </div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: '24px',
          }}>
            {products.map((product) => (
              <div key={product.id} className="card">
                <Link href={`/product/${product.id}`}>
                  <div style={{
                    height: '200px',
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
                </Link>
                <div style={{ padding: '20px' }}>
                  <span className="badge badge-yellow" style={{ marginBottom: '8px', display: 'inline-block' }}>
                    {categoryLabels[product.category] || product.category}
                  </span>
                  <Link href={`/product/${product.id}`}>
                    <h3 style={{
                      fontSize: '18px',
                      fontWeight: 'bold',
                      marginBottom: '8px',
                      color: '#111827',
                    }}>
                      {product.name}
                    </h3>
                  </Link>
                  <p style={{
                    fontSize: '14px',
                    color: '#6b7280',
                    marginBottom: '16px',
                    lineHeight: 1.5,
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                  }}>
                    {product.description}
                  </p>
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}>
                    <span style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: '#2563eb',
                    }}>
                      ¥{product.price.toFixed(2)}
                    </span>
                    <button
                      onClick={() => handleAddToCart(product.id)}
                      disabled={addingToCart === product.id}
                      className="btn btn-primary"
                      style={{ padding: '8px 16px', fontSize: '14px' }}
                    >
                      {addingToCart === product.id ? '添加中...' : '加入购物车'}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer style={{
        backgroundColor: '#1f2937',
        color: '#9ca3af',
        padding: '40px 20px',
        textAlign: 'center',
        marginTop: '60px',
      }}>
        <div className="container">
          <p>优选商城 - AI辅助编程与工程化实训项目</p>
          <p style={{ marginTop: '8px', fontSize: '14px' }}>
            技术栈：Next.js + Flask + SQLite
          </p>
        </div>
      </footer>
    </>
  );
}
