import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';
import AdminLayout from '../components/AdminLayout';
import ConfirmDialog from '../components/ConfirmDialog';

export default function Usuarios() {
    const [usuarios, setUsuarios] = useState([]);
    const [nome, setNome] = useState('');
    const [senha, setSenha] = useState('');
    const [cargo, setCargo] = useState('ADMINISTRADOR');

    // Estados do Modal de Edição
    const [usuarioParaEditar, setUsuarioParaEditar] = useState(null);
    const [editNome, setEditNome] = useState('');
    const [editCargo, setEditCargo] = useState('');
    const [isEditing, setIsEditing] = useState(false);

    // Estados de Confirmação
    const [usuarioParaDeletar, setUsuarioParaDeletar] = useState(null);
    const [isDeleting, setIsDeleting] = useState(false);

    // Estados de Transferência de Posse
    const [usuarioParaTransferir, setUsuarioParaTransferir] = useState(null);
    const [isTransferring, setIsTransferring] = useState(false);

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

    const cadastrarUsuario = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/api/usuarios/cadastrar', { nome, senha, cargo }, { withCredentials: true });
            if (response.data.success) {
                toast.success('✅ Usuário cadastrado com sucesso!');
                setNome(''); setSenha(''); setCargo('ADMINISTRADOR');
                fetchUsuarios();
            } else {
                toast.error(response.data.message || 'Erro ao cadastrar usuário.');
            }
        } catch (err) { toast.error('❌ Não foi possível cadastrar o usuário.'); }
    };

    // Edição de Usuário
    const abrirEdicao = (usuario) => {
        setUsuarioParaEditar(usuario);
        setEditNome(usuario.nome);
        setEditCargo(usuario.cargo);
    };

    const salvarEdicao = async () => {
        if (!usuarioParaEditar) return;
        if (!editNome.trim()) return toast.warning('Nome é obrigatório.');
        setIsEditing(true);
        try {
            const response = await axios.put(`http://localhost:5000/api/usuarios/editar_usuario/${usuarioParaEditar.id}`, {
                nome: editNome.trim(), cargo: editCargo
            }, { withCredentials: true });
            if (response.data.success) {
                toast.success('✏️ Usuário atualizado com sucesso!');
                setUsuarioParaEditar(null);
                fetchUsuarios();
            } else {
                toast.error(response.data.message || 'Erro ao editar usuário.');
            }
        } catch (err) {
            toast.error('❌ Não foi possível editar o usuário.');
        } finally {
            setIsEditing(false);
        }
    };

    // Deleção com Confirmação
    const confirmarDelecao = async () => {
        if (!usuarioParaDeletar) return;
        setIsDeleting(true);
        try {
            const response = await axios.delete(`http://localhost:5000/api/usuarios/deletar_usuario/${usuarioParaDeletar.id}`, { withCredentials: true });
            if (response.data.success) {
                toast.success('🗑️ Usuário removido com sucesso.');
                setUsuarioParaDeletar(null);
                fetchUsuarios();
            } else {
                toast.error(response.data.message || 'Erro ao excluir usuário.');
            }
        } catch (err) { toast.error('Erro ao excluir o usuário.'); }
        finally { setIsDeleting(false); }
    };

    // Transferência de Posse
    const confirmarTransferencia = async () => {
        if (!usuarioParaTransferir) return;
        setIsTransferring(true);
        try {
            const meuPerfil = await axios.get('http://localhost:5000/api/meu_perfil', { withCredentials: true });
            const meuId = meuPerfil.data.data?.id;
            if (!meuId) return toast.error('Erro ao identificar seu perfil.');

            const response = await axios.post('http://localhost:5000/api/usuarios/transferir_posse', {
                id_atual: meuId, id_novo: usuarioParaTransferir.id
            }, { withCredentials: true });
            if (response.data.success) {
                toast.success('🔑 Posse transferida com sucesso!');
                setUsuarioParaTransferir(null);
                fetchUsuarios();
            } else {
                toast.error(response.data.message || 'Erro ao transferir posse.');
            }
        } catch (err) { toast.error('❌ Não foi possível transferir a posse.'); }
        finally { setIsTransferring(false); }
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
                    <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} type="submit">+ Cadastrar</motion.button>
                </form>
            </div>

            <div className="grid-cards">
                <AnimatePresence>
                    {usuarios.map(usuario => (
                        <motion.div 
                            className="card" 
                            key={usuario.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, x: -10 }}
                        >
                            <h3>{usuario.nome}</h3>
                            <span className="status-badge">{usuario.cargo}</span>
                            <p style={{ fontFamily: "'Rubik',sans-serif", fontSize: '11px', color: '#555' }}>#{String(usuario.id).padStart(3, '0')}</p>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '14px' }}>
                                <button onClick={() => abrirEdicao(usuario)} style={{ width: '100%', background: '#444' }}>✏️ Editar</button>
                                <button onClick={() => setUsuarioParaDeletar(usuario)} className="danger" style={{ width: '100%' }}>Excluir</button>
                                {usuario.cargo !== 'ADMINISTRADOR' && (
                                    <button onClick={() => setUsuarioParaTransferir(usuario)} style={{ width: '100%', background: 'linear-gradient(90deg, #444400, #888800)', color: '#fff', fontSize: '10px' }}>🔑 Transferir Posse</button>
                                )}
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
                                    <option value="ADMINISTRADOR">Administrador</option>
                                    <option value="GARCOM">Garçom</option>
                                    <option value="COZINHEIRO">Cozinheiro</option>
                                </select>
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

            {/* Confirmação de Deleção */}
            <ConfirmDialog 
                isOpen={!!usuarioParaDeletar}
                title="Excluir usuário?"
                description={`Esta ação removerá o usuário "${usuarioParaDeletar?.nome}" do sistema. Deseja continuar?`}
                confirmLabel="Excluir usuário"
                cancelLabel="Cancelar"
                variant="danger"
                isLoading={isDeleting}
                onConfirm={confirmarDelecao}
                onCancel={() => setUsuarioParaDeletar(null)}
            />

            {/* Confirmação de Transferência de Posse */}
            <ConfirmDialog 
                isOpen={!!usuarioParaTransferir}
                title="⚠️ Transferir posse do sistema?"
                description={`Você está prestes a transferir a posse de Administrador para "${usuarioParaTransferir?.nome}". Seu cargo será rebaixado. Esta é uma ação sensível e irreversível.`}
                confirmLabel="Transferir posse"
                cancelLabel="Cancelar"
                variant="danger"
                isLoading={isTransferring}
                onConfirm={confirmarTransferencia}
                onCancel={() => setUsuarioParaTransferir(null)}
            />
        </AdminLayout>
    );
}