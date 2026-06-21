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
                    <Link to="/produtos" style={{ background: 'rgba(0,0,0,0.2)', color: '#fff' }}>Admin</Link>
                    <Link to="/salao">Salão</Link>
                    <Link to="/cozinha/fila">Cozinha</Link>
                    <button onClick={handleLogout} className="logout" style={{ background:'transparent', border:'none', cursor:'pointer', fontWeight:'bold', textTransform:'uppercase', letterSpacing:'1.5px', color:'#ffcccc' }}>Sair</button>
                </div>
            </nav>

            <div className="nav-tabs">
                <Link to="/produtos" className={location.pathname === '/produtos' ? 'active' : ''}>Produtos</Link>
                <Link to="/usuarios" className={location.pathname === '/usuarios' ? 'active' : ''}>Usuários</Link>
            </div>

            <div className="content-container">
                {children}
            </div>
        </>
    );
}