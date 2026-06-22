import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';
import AdminLayout from '../components/AdminLayout';

export default function Produtos() {
    const [produtos, setProdutos] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [nome, setNome] = useState('');
    const [preco, setPreco] = useState('');
    const [categoria, setCategoria] = useState('Bebida');
    const [preparationTime, setPreparationTime] = useState(15);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const fetchProdutos = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/produtos', { withCredentials: true });
            if (response.data.success) {
                setProdutos(response.data.data);
            }
        } catch (err) { 
            console.error(err);
            toast.error('Erro ao carregar os produtos.');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => { fetchProdutos(); }, []);

    const cadastrarProduto = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        try {
            const response = await axios.post('http://localhost:5000/api/produtos/cadastrar', { nome, preco, categoria, preparation_time_minutes: preparationTime }, { withCredentials: true });
            if (response.data.success) {
                toast.success('✅ Produto cadastrado com sucesso!');
                setNome(''); setPreco(''); setCategoria('Bebida'); setPreparationTime(15);
                fetchProdutos();
            } else {
                toast.error(response.data.message || 'Erro ao cadastrar produto.');
            }
        } catch (err) {
            toast.error('❌ Não foi possível concluir a ação.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const deletarProduto = async (id) => {
        try {
            const response = await axios.delete(`http://localhost:5000/api/produtos/deletar/${id}`, { withCredentials: true });
            if (response.data.success) {
                toast.success('🗑️ Produto removido com sucesso.');
                fetchProdutos();
            } else {
                toast.error(response.data.message || 'Erro ao deletar produto.');
            }
        } catch (err) {
            toast.error('Erro ao excluir o produto.');
        }
    };

    return (
        <AdminLayout>
            <h2 className="page-title">Gerenciar Produtos</h2>

            <div className="card">
                <form onSubmit={cadastrarProduto} className="form-row">
                    <input type="text" placeholder="Nome do produto" value={nome} onChange={e => setNome(e.target.value)} required style={{ flex: 1, minWidth: '160px' }} />
                    <input type="number" step="0.01" placeholder="Preço (R$)" value={preco} onChange={e => setPreco(e.target.value)} required style={{ width: '120px' }} />
                    <select value={categoria} onChange={e => setCategoria(e.target.value)} style={{ width: '140px' }}>
                        <option value="Bebida">Bebida</option>
                        <option value="Prato">Prato</option>
                        <option value="Sobremesa">Sobremesa</option>
                    </select>
                    <input type="number" placeholder="Tempo (min)" value={preparationTime} onChange={e => setPreparationTime(e.target.value)} required min="1" style={{ width: '100px' }} title="Tempo médio de preparo em minutos" />
                    <motion.button 
                        whileHover={{ scale: 1.02 }} 
                        whileTap={{ scale: 0.98 }} 
                        type="submit" 
                        disabled={isSubmitting}
                        style={{ opacity: isSubmitting ? 0.7 : 1 }}
                    >
                        {isSubmitting ? 'Cadastrando...' : '+ Cadastrar'}
                    </motion.button>
                </form>
            </div>

            <div className="card">
                <table>
                    <thead>
                        <tr>
                            <th style={{ width: '60px' }}>ID</th> 
                            <th>Produto</th>
                            <th>Categoria</th>
                            <th>Preço</th>
                            <th>Tempo</th>
                            <th style={{ textAlign: 'right' }}>Ação</th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ? (
                            Array.from({ length: 5 }).map((_, idx) => (
                                <tr key={`skeleton-${idx}`} className="skeleton-row">
                                    <td><div className="skeleton skeleton-text" style={{ width: '30px' }}></div></td>
                                    <td><div className="skeleton skeleton-text"></div></td>
                                    <td><div className="skeleton skeleton-text" style={{ width: '60px' }}></div></td>
                                    <td><div className="skeleton skeleton-text" style={{ width: '50px' }}></div></td>
                                    <td><div className="skeleton skeleton-text" style={{ width: '40px' }}></div></td>
                                    <td style={{ textAlign: 'right' }}>
                                        <div className="skeleton skeleton-btn" style={{ marginLeft: 'auto' }}></div>
                                    </td>
                                </tr>
                            ))
                        ) : produtos.length === 0 ? (
                            <tr>
                                <td colSpan="6" style={{ textAlign: 'center', padding: '20px', color: '#888', fontStyle: 'italic' }}>
                                    Nenhum produto cadastrado ainda.
                                </td>
                            </tr>
                        ) : (
                            <AnimatePresence>
                                {produtos.map((produto, idx) => (
                                    <motion.tr 
                                        key={produto.id}
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, x: -10 }}
                                        transition={{ duration: 0.2, delay: idx * 0.05 }}
                                    >
                                        <td style={{ fontFamily: "'Rubik',sans-serif", fontSize: '11px', color: '#555' }}>#{produto.id}</td>
                                        <td>{produto.nome}</td>
                                        <td style={{ color: 'var(--text-muted)' }}>{produto.categoria}</td>
                                        <td className="price-cell">R$ {parseFloat(produto.preco).toFixed(2)}</td>
                                        <td>{produto.preparation_time_minutes} min</td>
                                        <td style={{ textAlign: 'right' }}>
                                            <motion.button 
                                                whileHover={{ scale: 1.05 }} 
                                                whileTap={{ scale: 0.95 }}
                                                onClick={() => deletarProduto(produto.id)} 
                                                className="danger"
                                            >
                                                Excluir
                                            </motion.button>
                                        </td>
                                    </motion.tr>
                                ))}
                            </AnimatePresence>
                        )}
                    </tbody>
                </table>
            </div>
        </AdminLayout>
    );
}