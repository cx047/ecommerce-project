import Link from 'next/link';

export default function NotFound() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      textAlign: 'center',
      padding: '20px',
    }}>
      <h1 style={{ fontSize: '72px', fontWeight: 'bold', color: '#2563eb', marginBottom: '16px' }}>
        404
      </h1>
      <p style={{ fontSize: '20px', color: '#6b7280', marginBottom: '32px' }}>
        页面不存在
      </p>
      <Link href="/" className="btn btn-primary">
        返回首页
      </Link>
    </div>
  );
}
