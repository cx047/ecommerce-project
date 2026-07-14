import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: '优选商城 - 品质生活优选',
  description: '精选数码、服饰、家居好物，品质生活从这里开始',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
