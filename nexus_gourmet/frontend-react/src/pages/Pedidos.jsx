import React from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import KitchenOrdersPanel from '../components/KitchenOrdersPanel';
import '../assets/css/admin.css';
import logoSite2 from '../assets/img/logosite2.png';

export default function Pedidos() {
    const navigate = useNavigate();
    const cargo = localStorage.getItem('userCargo');

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    const concluirPedido = async (numero_mesa, comanda_id) => {
        await axios.put(`http://localhost:5000/api/cozinha/${comanda_id}/alterar_status`, 
        { status: 'Pronto' }, { withCredentials: true });
    };

    return (
        <>
            <nav className="navbar">
                <div className="logo" style={{ display: 'flex', alignItems: 'center' }}>
                    <img src={logoSite2} alt="Nexus Gourmet" style={{ height: '45px', width: 'auto', objectFit: 'contain' }} />
                </div>
                <div className="navbar-links">
                    {cargo === 'ADMINISTRADOR' && <Link to="/produtos">Admin</Link>}
                    {(cargo === 'ADMINISTRADOR' || cargo === 'GARCOM') && <Link to="/salao">Salão</Link>}
                    <Link to="/cozinha/fila" style={{ background: 'rgba(0,0,0,0.2)', color: '#fff' }}>Cozinha</Link>
                    <button onClick={handleLogout} className="logout" style={{ background:'transparent', border:'none', cursor:'pointer', fontWeight:'bold', color:'#ffcccc' }}>Sair</button>
                </div>
            </nav>

            <div className="content-container">
                <h2 className="page-title">Fila de Preparo</h2>
                <KitchenOrdersPanel onConcluirPedido={concluirPedido} />
            </div>
        </>
    );
}