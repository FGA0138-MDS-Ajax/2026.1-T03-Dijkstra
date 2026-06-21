import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Mesas from './pages/Mesas';
import Produtos from './pages/Produtos';
import Usuarios from './pages/Usuarios';
import Comandas from './pages/Comandas';
import Pedidos from './pages/Pedidos';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        
        {/* Admin */}
        <Route path="/produtos" element={<Produtos />} />
        <Route path="/usuarios" element={<Usuarios />} />
        
        {/* Salão */}
        <Route path="/salao" element={<Mesas />} />
        <Route path="/salao/:numero_mesa/comandas/:comanda_id" element={<Comandas />} />
        
        {/* Cozinha */}
        <Route path="/cozinha/fila" element={<Pedidos />} />
      </Routes>
    </Router>
  );
}

export default App;