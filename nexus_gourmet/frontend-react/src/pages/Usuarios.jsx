import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';
import AdminLayout from '../components/AdminLayout';
import ConfirmDialog from '../components/ConfirmDialog';

export default function Usuarios() {
    const [usuarios, setUsuarios] = useState([]);
    
    // Estados do Cadastro (Ajustado o valor inicial para bater com o Enum do Backend)
    const [nome, setNome] = useState('');
    const [cpf, setCpf] = useState('');
    const [senha, setSenha] = useState('');
    const [cargo, setCargo] = useState('Administrador');
    const [senhaAdmin, setSenhaAdmin] = useState('');

    // Estados do Modal de Edição
    const [usuarioParaEditar, setUsuarioParaEditar] = useState(null);
    const [editNome, setEditNome] = useState('');
    const [editCargo, setEditCargo] = useState('');
    const [editSenhaAdmin, setEditSenhaAdmin] = useState('');
    const [isEditing, setIsEditing] = useState(false);

    // Estados de Confirmação (Deleção)
    const [usuarioParaDeletar, setUsuarioParaDeletar] = useState(null);
    const [deleteSenhaAdmin, setDeleteSenhaAdmin] = useState('');
    const [isDeleting, setIsDeleting] = useState(false);

    const fetchUsuarios = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/usuarios', { withCredentials: true });
            if (response.data.success) setUsuarios(response.data.data);
        } catch (err) { 
            console.error(err); 
            toast.error('Erro ao carregar usuários.');
        }
    };

    useEffect(() => { fetchUsuarios(); }, []);

    // ─── CADASTRO ───
    const cadastrarUsuario = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/api/usuarios/cadastrar', { 
                nome, 
                cargo,
                cpf_cadastrado: cpf, 
                senha_cadastrada: senha, 
                senha_admin: senhaAdmin
            }, { withCredentials: true });

            if (response.data.success) {
                toast.success('✅ Usuário cadastrado com sucesso!');
                setNome(''); setCpf(''); setSenha(''); setCargo('Administrador'); setSenhaAdmin('');
                fetchUsuarios();
            } else {
                toast.error(response.data.message || 'Erro ao cadastrar usuário.');
            }
        } catch (err) { 
            toast.error(err.response?.data?.message || '❌ Não foi possível cadastrar o usuário. Verifique seus dados.'); 
        }
    };

    // ─── EDIÇÃO ───
    const abrirEdicao = (usuario) => {
        setUsuarioParaEditar(usuario);
        setEditNome(usuario.nome);
        setEditCargo(usuario.cargo);
        setEditSenhaAdmin('');
    };

    const salvarEdicao = async () => {
        if (!usuarioParaEditar) return;
        if (!editNome.trim()) return toast.warning('Nome é obrigatório.');
        if (!editSenhaAdmin) return toast.warning('A senha de administrador é obrigatória.');
        
        setIsEditing(true);
        try {
            const response = await axios.put(`http://localhost:5000/api/usuarios/editar_usuario/${usuarioParaEditar.cpf}`, {
                nome: editNome.trim(), 
                cargo: editCargo,
                senha_admin: editSenhaAdmin 
            }, { withCredentials: true });

            if (response.data.success) {
                toast.success('✏️ Usuário atualizado com sucesso!');
                setUsuarioParaEditar(null);
                fetchUsuarios();
            } else {
                toast.error(response.data.message || 'Erro ao editar usuário.');
            }
        } catch (err) {
            toast.error(err.response?.data?.message || '❌ Não foi possível editar o usuário.');
        } finally {
            setIsEditing(false);
        }
    };

    // ─── DELEÇÃO ───
    const confirmarDelecao = async () => {
        if (!usuarioParaDeletar) return;
        if (!deleteSenhaAdmin) return toast.warning('A senha do administrador é obrigatória para excluir.');

        setIsDeleting(true);
        try {
            const response = await axios.delete(`http://localhost:5000/api/usuarios/deletar_usuario/${usuarioParaDeletar.cpf}`, { 
                data: { senha_admin: deleteSenhaAdmin }, 
                withCredentials: true 
            });

            if (response.data.success) {
                toast.success('🗑️ Usuário removido com sucesso.');
                setUsuarioParaDeletar(null);
                setDeleteSenhaAdmin('');
                fetchUsuarios();
            } else {
                toast.error(response.data.message || 'Erro ao excluir usuário.');
            }
        } catch (err) { 
            toast.error(err.response?.data?.message || 'Erro ao excluir o usuário.'); 
        } finally { 
            setIsDeleting(false); 
        }
    };

    return (
        <AdminLayout>
            <h2 className="page-title">Usuários do Sistema</h2>

            <div className="card">
                <form onSubmit={cadastrarUsuario} className="form-row">
                    <input type="text" placeholder="Nome Completo" value={nome} onChange={e => setNome(e.target.value)} required style={{ flex: 1, minWidth: '160px' }} />
                    <input type="text" placeholder="CPF (Apenas números)" value={cpf} onChange={e => setCpf(e.target.value)} required style={{ width: '150px' }} />
                    <select value={cargo} onChange={e => setCargo(e.target.value)} style={{ width: '150px' }}>
                        {/* Values corrigidos para baterem com o Enum de Models */}
                        <option value="Administrador">Administrador</option>
                        <option value="Garçom">Garçom</option>
                        <option value="Cozinheiro">Cozinheiro</option>
                    </select>
                    <input type="password" placeholder="Senha do Usuário" value={senha} onChange={e => setSenha(e.target.value)} required style={{ width: '140px' }} />
                    
                    <div style={{ position: 'relative', width: '160px' }}>
                        <input type="password" placeholder="Sua Senha (Admin)" value={senhaAdmin} onChange={e => setSenhaAdmin(e.target.value)} required style={{ width: '100%', border: '1px solid var(--primary-red)' }} title="Senha de autorização de admin" />
                    </div>
                    
                    <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} type="submit">+ Cadastrar</motion.button>
                </form>
            </div>

            <div className="grid-cards">
                <AnimatePresence>
                    {usuarios.map(usuario => (
                        <motion.div 
                            className="card" 
                            key={usuario.cpf}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, x: -10 }}
                        >
                            <h3>{usuario.nome}</h3>
                            <span className="status-badge">{usuario.cargo}</span>
                            <p style={{ fontFamily: "'Rubik',sans-serif", fontSize: '11px', color: '#555' }}>CPF: {usuario.cpf}</p>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '14px' }}>
                                <button onClick={() => abrirEdicao(usuario)} style={{ width: '100%', background: '#444' }}>✏️ Editar</button>
                                <button onClick={() => setUsuarioParaDeletar(usuario)} className="danger" style={{ width: '100%' }}>Excluir</button>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>

            {/* Modal de Edição de Usuário */}
            {usuarioParaEditar && (
                <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.85)', zIndex: 9999, display: 'flex', justifyContent: 'center', alignItems: 'center', backdropFilter: 'blur(4px)' }}>
                    <motion.div 
                        initial={{ opacity: 0, scale: 0.95, y: 10 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        className="card" 
                        style={{ width: '90%', maxWidth: '400px', background: '#1a1a1a', border: '1px solid #333', boxShadow: '0 10px 40px rgba(0,0,0,0.5)', padding: '24px' }}
                    >
                        <h2 style={{ color: '#fff', fontSize: '18px', marginBottom: '20px' }}>Editar Usuário</h2>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                            <div>
                                <label style={{ fontSize: '11px', color: '#888', display: 'block', marginBottom: '4px' }}>Nome</label>
                                <input type="text" value={editNome} onChange={e => setEditNome(e.target.value)} style={{ width: '100%' }} required />
                            </div>
                            <div>
                                <label style={{ fontSize: '11px', color: '#888', display: 'block', marginBottom: '4px' }}>Cargo</label>
                                <select value={editCargo} onChange={e => setEditCargo(e.target.value)} style={{ width: '100%' }}>
                                    {/* Values corrigidos para baterem com o Enum de Models */}
                                    <option value="Administrador">Administrador</option>
                                    <option value="Garçom">Garçom</option>
                                    <option value="Cozinheiro">Cozinheiro</option>
                                </select>
                            </div>
                            <div style={{ marginTop: '10px' }}>
                                <label style={{ fontSize: '11px', color: 'var(--primary-red)', display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>Sua Senha de Admin (Autorização)</label>
                                <input type="password" placeholder="Sua senha para confirmar edição" value={editSenhaAdmin} onChange={e => setEditSenhaAdmin(e.target.value)} style={{ width: '100%', border: '1px solid var(--primary-red)' }} required />
                            </div>
                        </div>
                        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '20px' }}>
                            <button onClick={() => setUsuarioParaEditar(null)} disabled={isEditing} style={{ background: 'transparent', color: '#ccc', border: '1px solid #444', opacity: isEditing ? 0.5 : 1 }}>Cancelar</button>
                            <motion.button 
                                whileHover={!isEditing ? { scale: 1.02 } : {}} 
                                whileTap={!isEditing ? { scale: 0.98 } : {}}
                                onClick={salvarEdicao} 
                                disabled={isEditing}
                                style={{ opacity: isEditing ? 0.7 : 1, cursor: isEditing ? 'wait' : 'pointer' }}
                            >
                                {isEditing ? 'Salvando...' : '✔ Salvar Alterações'}
                            </motion.button>
                        </div>
                    </motion.div>
                </div>
            )}

            {/* Confirmação de Deleção com Senha */}
            <ConfirmDialog 
                isOpen={!!usuarioParaDeletar}
                title="Excluir usuário?"
                description={`Esta ação removerá permanentemente o usuário "${usuarioParaDeletar?.nome}" do sistema. Digite sua senha de administrador para autorizar a exclusão:`}
                confirmLabel="Excluir usuário"
                cancelLabel="Cancelar"
                variant="danger"
                isLoading={isDeleting}
                onConfirm={confirmarDelecao}
                onCancel={() => { setUsuarioParaDeletar(null); setDeleteSenhaAdmin(''); }}
            >
                <div>
                    <input 
                        type="password" 
                        placeholder="Senha do Administrador" 
                        value={deleteSenhaAdmin} 
                        onChange={e => setDeleteSenhaAdmin(e.target.value)} 
                        style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #cc0000', background: '#000', color: '#fff', fontFamily: 'Rubik, sans-serif' }} 
                        required 
                    />
                </div>
            </ConfirmDialog>
        </AdminLayout>
    );
}