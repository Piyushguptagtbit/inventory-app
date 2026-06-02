import React, { useEffect, useState } from 'react';
import { getProducts, createProduct, updateProduct, deleteProduct } from '../api/client';
import toast from 'react-hot-toast';

const emptyForm = { name: '', sku: '', description: '', price: '', stock: '' };

export default function Products() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editing, setEditing] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const load = async () => {
    const res = await getProducts();
    setProducts(res.data);
  };
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = { ...form, price: parseFloat(form.price), stock: parseInt(form.stock) };
    try {
      if (editing) {
        await updateProduct(editing, payload);
        toast.success('Product updated!');
      } else {
        await createProduct(payload);
        toast.success('Product created!');
      }
      setForm(emptyForm); setEditing(null); setShowForm(false); load();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Error');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this product?')) return;
    await deleteProduct(id);
    toast.success('Deleted');
    load();
  };

  const startEdit = (p) => {
    setForm({ name: p.name, sku: p.sku, description: p.description, price: p.price, stock: p.stock });
    setEditing(p.id); setShowForm(true);
  };

  return (
    <div>
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:16 }}>
        <h2 style={{ margin:0 }}>📦 Products</h2>
        <button className="btn-primary" onClick={() => { setShowForm(!showForm); setEditing(null); setForm(emptyForm); }}>
          {showForm ? 'Cancel' : '+ Add Product'}
        </button>
      </div>

      {showForm && (
        <form className="card" onSubmit={handleSubmit} style={{ marginBottom:24 }}>
          <h3 style={{ marginTop:0 }}>{editing ? 'Edit Product' : 'New Product'}</h3>
          <div className="form-grid">
            <div><label>Name *</label><input required value={form.name} onChange={e => setForm({...form, name:e.target.value})} /></div>
            <div><label>SKU *</label><input required value={form.sku} onChange={e => setForm({...form, sku:e.target.value})} /></div>
            <div><label>Price *</label><input required type="number" min="0" step="0.01" value={form.price} onChange={e => setForm({...form, price:e.target.value})} /></div>
            <div><label>Stock *</label><input required type="number" min="0" value={form.stock} onChange={e => setForm({...form, stock:e.target.value})} /></div>
            <div style={{ gridColumn:'1/-1' }}><label>Description</label><input value={form.description} onChange={e => setForm({...form, description:e.target.value})} /></div>
          </div>
          <button className="btn-primary" type="submit" style={{ marginTop:12 }}>{editing ? 'Update' : 'Create'}</button>
        </form>
      )}

      <div className="table-wrap">
        <table>
          <thead><tr><th>ID</th><th>Name</th><th>SKU</th><th>Price</th><th>Stock</th><th>Actions</th></tr></thead>
          <tbody>
            {products.map(p => (
              <tr key={p.id}>
                <td>{p.id}</td><td>{p.name}</td><td><code>{p.sku}</code></td>
                <td>₹{p.price.toFixed(2)}</td>
                <td><span className={p.stock < 5 ? 'badge-red' : 'badge-green'}>{p.stock}</span></td>
                <td>
                  <button className="btn-sm" onClick={() => startEdit(p)}>Edit</button>
                  <button className="btn-sm btn-danger" onClick={() => handleDelete(p.id)}>Delete</button>
                </td>
              </tr>
            ))}
            {products.length === 0 && <tr><td colSpan={6} style={{textAlign:'center',color:'#888'}}>No products yet</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
