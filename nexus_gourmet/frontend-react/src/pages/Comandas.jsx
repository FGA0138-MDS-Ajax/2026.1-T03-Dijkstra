import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';
import SalaoLayout from '../components/SalaoLayout';

export default function Comandas() {
    const { numero_mesa, comanda_id } = useParams();
    const navigate = useNavigate();
    
    const [comanda, setComanda] = useState(null);
    const [produtosDisponiveis, setProdutosDisponiveis] = useState([]);
    const [produtoId, setProdutoId] = useState('');
    const [quantidade, setQuantidade] = useState(1);

    const [isLoading, setIsLoading] = useState(true);

    const fetchData = async () => {
        try {
            const [resComanda, resProdutos] = await Promise.all([
                axios.get(`http://localhost:5000/api/salao/${numero_mesa}/comandas/${comanda_id}`, { withCredentials: true }),
                axios.get('http://localhost:5000/api/produtos', { withCredentials: true })
            ]);
            if (resComanda.data.success) setComanda(resComanda.data.data);
            if (resProdutos.data.success) setProdutosDisponiveis(resProdutos.data.data);
        } catch (err) {
            console.error(err);
            toast.error('Erro ao carregar os dados da comanda.');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, [numero_mesa, comanda_id]);

    const adicionarProduto = async (e) => {
        e.preventDefault();
        try {
            await axios.post(`http://localhost:5000/api/salao/${numero_mesa}/comandas/${comanda_id}/adicionar_item`, 
                { product_id: produtoId, quantidade, observacao: '' }, { withCredentials: true });
            toast.success('➕ Produto adicionado à comanda.');
            setProdutoId(''); setQuantidade(1);
            fetchData();
        } catch (err) { toast.error('Erro ao adicionar produto.'); }
    };

    const enviarParaCozinha = async () => {
        try {
            await axios.post(`http://localhost:5000/api/salao/${numero_mesa}/comandas/${comanda_id}/enviar_comanda`, {}, { withCredentials: true });
            toast.success('🍽️ Pedido enviado para a cozinha.');
            navigate('/salao');
        } catch (err) { toast.error('Erro ao enviar pedido.'); }
    };

    const fecharConta = async () => {
        try {
            await axios.post(`http://localhost:5000/api/salao/${numero_mesa}/comandas/${comanda_id}/fechar`, {}, { withCredentials: true });
            toast.success('✅ Conta fechada com sucesso.');
            navigate('/salao');
        } catch (err) { toast.error("AVISO: Todos os pedidos dessa comanda devem constar como 'Entregue' para poder fechar a conta."); }
    };

    const totalComanda = comanda?.itens?.reduce((acc, item) => acc + (item.quantidade * (item.produto?.preco || 0)), 0) || 0;

    return (
        <SalaoLayout>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <h2 className="page-title" style={{ marginBottom: 0, border: 'none' }}>Comanda - Mesa {numero_mesa}</h2>
                <Link to="/salao"><button className="danger">Voltar às Mesas</button></Link>
            </div>

            <div className="card">
                <h3>Adicionar Produto</h3>
                <form onSubmit={adicionarProduto} className="form-row" style={{ marginTop: '15px' }}>
                    <select value={produtoId} onChange={e => setProdutoId(e.target.value)} style={{ flex: 1, minWidth: '200px' }} required>
                        <option value="" disabled>Selecione um produto...</option>
                        {produtosDisponiveis.map(prod => (
                            <option key={prod.id} value={prod.id}>{prod.nome} - R$ {parseFloat(prod.preco).toFixed(2)}</option>
                        ))}
                    </select>
                    <input type="number" value={quantidade} onChange={e => setQuantidade(e.target.value)} min="1" style={{ width: '80px' }} required />
                    <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} type="submit">+ Adicionar</motion.button>
                </form>
            </div>

            {comanda && (
                <div className="card">
                    <h3>Itens na Comanda (Status: {comanda.status})</h3>
                    <table style={{ marginTop: '15px' }}>
                        <thead>
                            <tr>
                                <th>Qtd</th>
                                <th>Produto</th>
                                <th style={{ textAlign: 'right' }}>Subtotal</th>
                            </tr>
                        </thead>
                        <tbody>
                            {isLoading ? (
                                Array.from({ length: 3 }).map((_, idx) => (
                                    <tr key={`skel-${idx}`} className="skeleton-row">
                                        <td><div className="skeleton skeleton-text" style={{ width: '30px' }}></div></td>
                                        <td><div className="skeleton skeleton-text"></div></td>
                                        <td style={{ textAlign: 'right' }}><div className="skeleton skeleton-text" style={{ width: '50px', marginLeft: 'auto' }}></div></td>
                                    </tr>
                                ))
                            ) : (
                                <AnimatePresence>
                                    {comanda.itens.map(item => (
                                        <motion.tr 
                                            key={item.id}
                                            initial={{ opacity: 0, y: 5 }}
                                            animate={{ opacity: 1, y: 0 }}
                                        >
                                            <td>{item.quantidade}x</td>
                                            <td>{item.produto?.nome}</td>
                                            <td className="price-cell" style={{ textAlign: 'right' }}>
                                                R$ {(item.quantidade * (item.produto?.preco || 0)).toFixed(2)}
                                            </td>
                                        </motion.tr>
                                    ))}
                                </AnimatePresence>
                            )}
                        </tbody>
                    </table>
                    
                    <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #3a0000', paddingTop: '15px' }}>
                        <h3 style={{ color: 'var(--primary-red)' }}>Total: R$ {totalComanda.toFixed(2)}</h3>
                        <div>
                            {comanda.status === 'Entregue' && <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={fecharConta} className="danger" style={{ marginRight: '10px' }}>Fechar Conta</motion.button>}
                            <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={enviarParaCozinha}>Enviar Pedido para Cozinha</motion.button>
                        </div>
                    </div>
                </div>
            )}
        </SalaoLayout>
    );
}