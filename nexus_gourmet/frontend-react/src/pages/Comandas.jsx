import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link, useNavigate } from 'react-router-dom';
import SalaoLayout from '../components/SalaoLayout';

export default function Comandas() {
    const { numero_mesa, comanda_id } = useParams();
    const navigate = useNavigate();
    
    const [comanda, setComanda] = useState(null);
    const [produtosDisponiveis, setProdutosDisponiveis] = useState([]);
    const [produtoId, setProdutoId] = useState('');
    const [quantidade, setQuantidade] = useState(1);

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
        }
    };

    useEffect(() => { fetchData(); }, [numero_mesa, comanda_id]);

    const adicionarProduto = async (e) => {
        e.preventDefault();
        await axios.post(`http://localhost:5000/api/salao/${numero_mesa}/comandas/${comanda_id}/adicionar_item`, 
            { product_id: produtoId, quantidade, observacao: '' }, { withCredentials: true });
        setProdutoId(''); setQuantidade(1);
        fetchData();
    };

    const enviarParaCozinha = async () => {
        await axios.post(`http://localhost:5000/api/salao/${numero_mesa}/comandas/${comanda_id}/enviar_comanda`, {}, { withCredentials: true });
        navigate('/salao');
    };

    const fecharConta = async () => {
        await axios.post(`http://localhost:5000/api/salao/${numero_mesa}/comandas/${comanda_id}/fechar`, {}, { withCredentials: true });
        navigate('/salao');
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
                    <button type="submit">+ Adicionar</button>
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
                            {comanda.itens.map(item => (
                                <tr key={item.id}>
                                    <td>{item.quantidade}x</td>
                                    <td>{item.produto?.nome}</td>
                                    <td className="price-cell" style={{ textAlign: 'right' }}>
                                        R$ {(item.quantidade * (item.produto?.preco || 0)).toFixed(2)}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    
                    <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #3a0000', paddingTop: '15px' }}>
                        <h3 style={{ color: 'var(--primary-red)' }}>Total: R$ {totalComanda.toFixed(2)}</h3>
                        <div>
                            {comanda.status === 'Entregue' && <button onClick={fecharConta} className="danger" style={{ marginRight: '10px' }}>Fechar Conta</button>}
                            <button onClick={enviarParaCozinha}>Enviar Pedido para Cozinha</button>
                        </div>
                    </div>
                </div>
            )}
        </SalaoLayout>
    );
}