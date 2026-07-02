import React from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import '../assets/css/admin.css';
import logoSite2 from '../assets/img/logosite2.png';

export default function AdminLayout({ children }) {
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    return (
        <>
            <nav className="navbar">
                <div className="logo" style={{ display: 'flex', alignItems: 'center' }}>
                    <img src={logoSite2} alt="Nexus Gourmet" style={{ height: '45px', width: 'auto', objectFit: 'contain' }} />
                </div>
                <div className="navbar-links">
                    <Link to="/produtos">Admin</Link>
                    <Link to="/salao">Salão</Link>
                    <Link to="/cozinha/fila">Cozinha</Link>
                    <button onClick={handleLogout} className="logout">Sair</button>
                </div>
            </nav>

            <div className="nav-tabs">
                <Link to="/produtos" className={location.pathname === '/produtos' ? 'active' : ''}>Produtos</Link>
                <Link to="/usuarios" className={location.pathname === '/usuarios' ? 'active' : ''}>Usuários</Link>
                <Link to="/dashboard" className={location.pathname === '/dashboard' ? 'active' : ''}>Dashboard</Link>
            </div>

            <div className="content-container">
                {children}
            </div>
        </>
    );
}