import React, { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import Products from './pages/Products';
import Customers from './pages/Customers';
import Orders from './pages/Orders';
import './App.css';

export default function App() {
  const [tab, setTab] = useState('products');

  return (
    <div className="app">
      <Toaster position="top-right" />
      <header className="header">
        <div className="header-inner">
          <div className="logo">🏭 Inventory & Order Manager</div>
          <nav className="nav">
            {['products','customers','orders'].map(t => (
              <button key={t} className={`nav-btn ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>
                {t === 'products' ? '📦 Products' : t === 'customers' ? '👥 Customers' : '🛒 Orders'}
              </button>
            ))}
          </nav>
        </div>
      </header>
      <main className="main">
        {tab === 'products' && <Products />}
        {tab === 'customers' && <Customers />}
        {tab === 'orders' && <Orders />}
      </main>
    </div>
  );
}
