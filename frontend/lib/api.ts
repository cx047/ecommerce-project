const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000/api';

function getSessionId(): string {
  let sessionId = localStorage.getItem('session_id');
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem('session_id', sessionId);
  }
  return sessionId;
}

async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-Session-ID': getSessionId(),
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
}

// Product APIs
export function getProducts(category?: string, search?: string) {
  const params = new URLSearchParams();
  if (category) params.append('category', category);
  if (search) params.append('search', search);
  const query = params.toString();
  return fetchAPI(`/products${query ? '?' + query : ''}`);
}

export function getProduct(id: number) {
  return fetchAPI(`/products/${id}`);
}

export function getCategories() {
  return fetchAPI('/products/categories');
}

// Cart APIs
export function getCart() {
  return fetchAPI('/cart');
}

export function addToCart(productId: number, quantity: number = 1) {
  return fetchAPI('/cart', {
    method: 'POST',
    body: JSON.stringify({ product_id: productId, quantity }),
  });
}

export function updateCartItem(itemId: number, quantity: number) {
  return fetchAPI(`/cart/${itemId}`, {
    method: 'PUT',
    body: JSON.stringify({ quantity }),
  });
}

export function removeFromCart(itemId: number) {
  return fetchAPI(`/cart/${itemId}`, {
    method: 'DELETE',
  });
}

export function clearCart() {
  return fetchAPI('/cart/clear', {
    method: 'DELETE',
  });
}

// Order APIs
export function getOrders() {
  return fetchAPI('/orders');
}

export function createOrder(customerName?: string, customerEmail?: string) {
  return fetchAPI('/orders', {
    method: 'POST',
    body: JSON.stringify({ customer_name: customerName, customer_email: customerEmail }),
  });
}

export function getOrder(id: number) {
  return fetchAPI(`/orders/${id}`);
}
