import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AdminLayout from '../components/AdminLayout';

export default function Usuarios() {
    const [usuarios, setUsuarios] = useState([]);
    const [nome, setNome] = useState('');
    const [senha, setSenha] = useState('');
    const [cargo, setCargo] = useState('ADMINISTRADOR');

    const fetchUsuarios = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/usuarios', { withCredentials: true });
            if (response.data.success) setUsuarios(response.data.data);
        } catch (err) { console.error(err); }
    };

    useEffect(() => { fetchUsuarios(); }, []);

    const cadastrarUsuario = async (e) => {
        e.preventDefault();
        await axios.post('http://localhost:5000/api/usuarios/cadastrar', { nome, senha, cargo }, { withCredentials: true });
        setNome(''); setSenha(''); setCargo('ADMINISTRADOR');
        fetchUsuarios();
    };

    const deletarUsuario = async (id) => {
        await axios.delete(`http://localhost:5000/api/usuarios/deletar_usuario/${id}`, { withCredentials: true });
        fetchUsuarios();
    };

    return (
        <AdminLayout>
            <h2 className="page-title">Usuários do Sistema</h2>

            <div className="card">
                <form onSubmit={cadastrarUsuario} className="form-row">
                    <input type="text" placeholder="Nome Completo" value={nome} onChange={e => setNome(e.target.value)} required style={{ flex: 1, minWidth: '160px' }} />
                    <input type="password" placeholder="Senha" value={senha} onChange={e => setSenha(e.target.value)} required style={{ width: '140px' }} />
                    <select value={cargo} onChange={e => setCargo(e.target.value)} style={{ width: '160px' }}>
                        <option value="ADMINISTRADOR">Administrador</option>
                        <option value="GARCOM">Garçom</option>
                        <option value="COZINHEIRO">Cozinheiro</option>
                    </select>
                    <button type="submit">+ Cadastrar</button>
                </form>
            </div>

            <div className="grid-cards">
                {usuarios.map(usuario => (
                    <div className="card" key={usuario.id}>
                        <h3>{usuario.nome}</h3>
                        <span className="status-badge">{usuario.cargo}</span>
                        <p style={{ fontFamily: "'Rubik',sans-serif", fontSize: '11px', color: '#555' }}>#{String(usuario.id).padStart(3, '0')}</p>
                        <button onClick={() => deletarUsuario(usuario.id)} className="danger" style={{ width: '100%', marginTop: '14px' }}>Excluir</button>
                    </div>
                ))}
            </div>
        </AdminLayout>
    );
}