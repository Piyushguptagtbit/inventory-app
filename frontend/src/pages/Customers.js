import React, { useEffect, useState } from 'react';
import { getCustomers, createCustomer, updateCustomer, deleteCustomer } from '../api/client';
import toast from 'react-hot-toast';

const emptyForm = { name: '', email: '', phone: '', address: '' };

export default function Customers() {
  const [customers, setCustomers] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editing, setEditing] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const load = async () => { const res = await getCustomers(); setCustomers(res.data); };
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) { await updateCustomer(editing, form); toast.success('Updated!'); }
      else { await createCustomer(form); toast.success('Customer created!'); }
      setForm(emptyForm); setEditing(null); setShowForm(false); load();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Error');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete?')) return;
    await deleteCustomer(id); toast.success('Deleted'); load();
  };

  const startEdit = (c) => {
    setForm({ name: c.name, email: c.email, phone: c.phone, address: c.address });
    setEditing(c.id); setShowForm(true);
  };

  return (
    <div>
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:16 }}>
        <h2 style={{ margin:0 }}>👥 Customers</h2>
        <button className="btn-primary" onClick={() => { setShowForm(!showForm); setEditing(null); setForm(emptyForm); }}>
          {showForm ? 'Cancel' : '+ Add Customer'}
        </button>
      </div>

      {showForm && (
        <form className="card" onSubmit={handleSubmit} style={{ marginBottom:24 }}>
          <h3 style={{ marginTop:0 }}>{editing ? 'Edit Customer' : 'New Customer'}</h3>
          <div className="form-grid">
            <div><label>Name *</label><input required value={form.name} onChange={e => setForm({...form, name:e.target.value})} /></div>
            <div><label>Email *</label><input required type="email" value={form.email} onChange={e => setForm({...form, email:e.target.value})} /></div>
            <div><label>Phone</label><input value={form.phone} onChange={e => setForm({...form, phone:e.target.value})} /></div>
            <div><label>Address</label><input value={form.address} onChange={e => setForm({...form, address:e.target.value})} /></div>
          </div>
          <button className="btn-primary" type="submit" style={{ marginTop:12 }}>{editing ? 'Update' : 'Create'}</button>
        </form>
      )}

      <div className="table-wrap">
        <table>
          <thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Actions</th></tr></thead>
          <tbody>
            {customers.map(c => (
              <tr key={c.id}>
                <td>{c.id}</td><td>{c.name}</td><td>{c.email}</td><td>{c.phone}</td>
                <td>
                  <button className="btn-sm" onClick={() => startEdit(c)}>Edit</button>
                  <button className="btn-sm btn-danger" onClick={() => handleDelete(c.id)}>Delete</button>
                </td>
              </tr>
            ))}
            {customers.length === 0 && <tr><td colSpan={5} style={{textAlign:'center',color:'#888'}}>No customers yet</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
