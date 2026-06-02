import React, { useEffect, useState } from 'react';
import { getOrders, getProducts, getCustomers, createOrder } from '../api/client';
import toast from 'react-hot-toast';

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [customerId, setCustomerId] = useState('');
  const [items, setItems] = useState([{ product_id: '', quantity: 1 }]);

  const load = async () => {
    const [o, p, c] = await Promise.all([getOrders(), getProducts(), getCustomers()]);
    setOrders(o.data); setProducts(p.data); setCustomers(c.data);
  };
  useEffect(() => { load(); }, []);

  const addItem = () => setItems([...items, { product_id: '', quantity: 1 }]);
  const removeItem = (i) => setItems(items.filter((_, idx) => idx !== i));
  const updateItem = (i, field, val) => {
    const updated = [...items];
    updated[i][field] = field === 'quantity' ? parseInt(val) : val;
    setItems(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!customerId) { toast.error('Select a customer'); return; }
    const validItems = items.filter(i => i.product_id && i.quantity > 0);
    if (!validItems.length) { toast.error('Add at least one item'); return; }
    try {
      await createOrder({ customer_id: parseInt(customerId), items: validItems.map(i => ({ product_id: parseInt(i.product_id), quantity: i.quantity })) });
      toast.success('Order placed!');
      setShowForm(false); setCustomerId(''); setItems([{ product_id: '', quantity: 1 }]);
      load();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Error placing order');
    }
  };

  const getCustomerName = (id) => customers.find(c => c.id === id)?.name || 'Unknown';

  return (
    <div>
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:16 }}>
        <h2 style={{ margin:0 }}>🛒 Orders</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Order'}</button>
      </div>

      {showForm && (
        <form className="card" onSubmit={handleSubmit} style={{ marginBottom:24 }}>
          <h3 style={{ marginTop:0 }}>New Order</h3>
          <div style={{ marginBottom:12 }}>
            <label>Customer *</label>
            <select value={customerId} onChange={e => setCustomerId(e.target.value)} required style={{ width:'100%', padding:'8px', borderRadius:6, border:'1px solid #ddd' }}>
              <option value="">Select customer...</option>
              {customers.map(c => <option key={c.id} value={c.id}>{c.name} ({c.email})</option>)}
            </select>
          </div>
          <label>Order Items</label>
          {items.map((item, i) => (
            <div key={i} style={{ display:'flex', gap:8, marginBottom:8, alignItems:'center' }}>
              <select value={item.product_id} onChange={e => updateItem(i, 'product_id', e.target.value)} style={{ flex:2, padding:'8px', borderRadius:6, border:'1px solid #ddd' }}>
                <option value="">Select product...</option>
                {products.map(p => <option key={p.id} value={p.id}>{p.name} (Stock: {p.stock}) - ₹{p.price}</option>)}
              </select>
              <input type="number" min="1" value={item.quantity} onChange={e => updateItem(i, 'quantity', e.target.value)} style={{ flex:1, padding:'8px', borderRadius:6, border:'1px solid #ddd' }} />
              {items.length > 1 && <button type="button" className="btn-sm btn-danger" onClick={() => removeItem(i)}>✕</button>}
            </div>
          ))}
          <button type="button" className="btn-sm" onClick={addItem} style={{ marginBottom:12 }}>+ Add Item</button>
          <br />
          <button className="btn-primary" type="submit">Place Order</button>
        </form>
      )}

      <div className="table-wrap">
        <table>
          <thead><tr><th>ID</th><th>Customer</th><th>Status</th><th>Total</th><th>Items</th><th>Date</th></tr></thead>
          <tbody>
            {orders.map(o => (
              <tr key={o.id}>
                <td>#{o.id}</td>
                <td>{getCustomerName(o.customer_id)}</td>
                <td><span className="badge-green">{o.status}</span></td>
                <td>₹{o.total_amount.toFixed(2)}</td>
                <td>{o.items?.length || 0} items</td>
                <td>{new Date(o.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
            {orders.length === 0 && <tr><td colSpan={6} style={{textAlign:'center',color:'#888'}}>No orders yet</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
