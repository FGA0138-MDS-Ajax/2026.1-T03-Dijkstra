import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import '../assets/css/admin.css';
import logoSite2 from '../assets/img/logosite2.png';

export default function Pedidos() {
    const [pedidos, setPedidos] = useState([]);
    const navigate = useNavigate();
    const cargo = localStorage.getItem('userCargo');

    const fetchPedidos = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/cozinha/fila', { withCredentials: true });
            if (response.data.success) {
                const emPreparo = response.data.data.filter(p => p.status === 'Em Preparo');
                setPedidos(emPreparo);
            }
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => { fetchPedidos(); }, []);

    const concluirPedido = async (numero_mesa, comanda_id) => {
        await axios.put(`http://localhost:5000/api/salao/${numero_mesa}/comandas/${comanda_id}/alterar_status`, 
            { status: 'Pronto' }, { withCredentials: true });
        fetchPedidos();
    };

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
                    {cargo === 'ADMINISTRADOR' && <Link to="/produtos">Admin</Link>}
                    {(cargo === 'ADMINISTRADOR' || cargo === 'GARCOM') && <Link to="/salao">Salão</Link>}
                    <Link to="/cozinha/fila" style={{ background: 'rgba(0,0,0,0.2)', color: '#fff' }}>Cozinha</Link>
                    <button onClick={handleLogout} className="logout" style={{ background:'transparent', border:'none', cursor:'pointer', fontWeight:'bold', color:'#ffcccc' }}>Sair</button>
                </div>
            </nav>

            <div className="content-container">
                <h2 className="page-title">Fila de Preparo</h2>
                <div className="grid-cards">
                    {pedidos.map(pedido => (
                        <div className="card" key={pedido.id} style={{ borderLeft: '4px solid var(--primary-red)' }}>
                            <h3>Mesa {pedido.mesa?.numero}</h3>
                            <span className="status-badge" style={{ background: '#331a00', color: '#ff9900' }}>A Preparar</span>
                            
                            <ul style={{ fontFamily: "'Rubik',sans-serif", fontSize: '13px', color: 'var(--text-dim)', margin: '10px 0 15px 20px' }}>
                                {pedido.itens.map(item => (
                                    <li key={item.id}>{item.quantidade}x - {item.produto}</li>
                                ))}
                            </ul>

                            <button 
                                onClick={() => concluirPedido(pedido.mesa?.numero, pedido.id)} 
                                style={{ 
                                    width: '100%', 
                                    background: 'linear-gradient(90deg, #004a00, #008b00)',
                                    whiteSpace: 'normal', /* Libera a quebra de linha */
                                    lineHeight: '1.4',    /* Ajusta a altura da linha caso ela quebre */
                                    padding: '10px 5px',  /* Reduz ligeiramente o espaçamento interno */
                                    textAlign: 'center'
                                }}
                            >
                                Marcar como Pronto
                            </button>
                        </div>
                    ))}
                    {pedidos.length === 0 && <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Nenhum pedido pendente no momento.</p>}
                </div>
            </div>
        </>
    );
}