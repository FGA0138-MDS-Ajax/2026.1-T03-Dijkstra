import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AdminLayout from '../components/AdminLayout';

export default function Produtos() {
    const [produtos, setProdutos] = useState([]);
    const [nome, setNome] = useState('');
    const [preco, setPreco] = useState('');
    const [categoria, setCategoria] = useState('Bebida');
    const [preparationTime, setPreparationTime] = useState(15);

    const fetchProdutos = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/produtos', { withCredentials: true });
            if (response.data.success) setProdutos(response.data.data);
        } catch (err) { console.error(err); }
    };

    useEffect(() => { fetchProdutos(); }, []);

    const cadastrarProduto = async (e) => {
        e.preventDefault();
        await axios.post('http://localhost:5000/api/produtos/cadastrar', { nome, preco, categoria, preparation_time_minutes: preparationTime }, { withCredentials: true });
        setNome(''); setPreco(''); setCategoria('Bebida'); setPreparationTime(15);
        fetchProdutos();
    };

    const deletarProduto = async (id) => {
        await axios.delete(`http://localhost:5000/api/produtos/deletar/${id}`, { withCredentials: true });
        fetchProdutos();
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
                    <button type="submit">+ Cadastrar</button>
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
                        {produtos.map(produto => (
                            <tr key={produto.id}>
                                <td style={{ fontFamily: "'Rubik',sans-serif", fontSize: '11px', color: '#555' }}>#{produto.id}</td>
                                <td>{produto.nome}</td>
                                <td style={{ color: 'var(--text-muted)' }}>{produto.categoria}</td>
                                <td className="price-cell">R$ {parseFloat(produto.preco).toFixed(2)}</td>
                                <td>{produto.preparation_time_minutes} min</td>
                                <td style={{ textAlign: 'right' }}>
                                    <button onClick={() => deletarProduto(produto.id)} className="danger">Excluir</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </AdminLayout>
    );
}