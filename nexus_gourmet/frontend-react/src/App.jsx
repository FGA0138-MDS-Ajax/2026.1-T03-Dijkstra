import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Mesas from './pages/Mesas';
import Comandas from './pages/Comandas';
import Pedidos from './pages/Pedidos';
import Produtos from './pages/Produtos';
import Usuarios from './pages/Usuarios';
import Dashboard from './pages/Dashboard';
import { Toaster } from 'sonner';

function App() {
  return (
    <>
      <Toaster richColors position="top-right" />
      <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/salao" element={<Mesas />} />
        <Route path="/salao/:numero_mesa/comandas/:comanda_id" element={<Comandas />} />
        <Route path="/cozinha/fila" element={<Pedidos />} />
        <Route path="/produtos" element={<Produtos />} />
        <Route path="/usuarios" element={<Usuarios />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
    </>
  );
}

export default App;
