import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import '../assets/css/admin.css';
import logoSite2 from '../assets/img/logosite2.png';

export default function SalaoLayout({ children }) {
    const navigate = useNavigate();
    const cargo = localStorage.getItem('userCargo');

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
                    {cargo === 'ADMINISTRADOR' && (
                        <>
                            <Link to="/produtos">Admin</Link>
                            <Link to="/salao" style={{ background: 'rgba(0,0,0,0.2)', color: '#fff' }}>Salão</Link>
                            <Link to="/cozinha/fila">Cozinha</Link>
                        </>
                    )}
                    {cargo === 'GARCOM' && <Link to="/salao" style={{ background: 'rgba(0,0,0,0.2)', color: '#fff' }}>Salão</Link>}
                    {cargo === 'COZINHEIRO' && <Link to="/cozinha/fila" style={{ background: 'rgba(0,0,0,0.2)', color: '#fff' }}>Cozinha</Link>}
                    <button onClick={handleLogout} className="logout" style={{ background:'transparent', border:'none', cursor:'pointer', fontWeight:'bold', textTransform:'uppercase', letterSpacing:'1.5px', color:'#ffcccc' }}>Sair</button>
                </div>
            </nav>

            <div className="content-container">
                {children}
            </div>
        </>
    );
}