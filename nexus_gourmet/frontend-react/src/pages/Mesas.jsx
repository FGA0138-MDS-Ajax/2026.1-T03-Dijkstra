import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';
import SalaoLayout from '../components/SalaoLayout';

export default function Mesas() {
    const [mesas, setMesas] = useState([]);
    const [produtos, setProdutos] = useState({ Bebida: [], Prato: [], Sobremesa: [] });
    const [isLoading, setIsLoading] = useState(true);
    const cargo = localStorage.getItem('userCargo');
    
    // Estados da Interface de Comandas
    const [expandedMesa, setExpandedMesa] = useState(null);
    const [comandasMesa, setComandasMesa] = useState([]);
    const [selectedComanda, setSelectedComanda] = useState(null);
    const [activeTab, setActiveTab] = useState('Prato');
    
    // Estados do CRUD de Mesas (Admin)
    const [novaCapacidade, setNovaCapacidade] = useState('');
    const [editingMesaNum, setEditingMesaNum] = useState(null);
    const [editCapacidade, setEditCapacidade] = useState('');

    // Estados do Modal de Pagamento (Caixa)
    const [modalConta, setModalConta] = useState(null);
    const [metodoPagamento, setMetodoPagamento] = useState('PIX');

    // Carrinho local por Comanda
    const [cart, setCart] = useState({});

    const fetchData = async () => {
        try {
            const resMesas = await axios.get('http://localhost:5000/api/salao', { withCredentials: true });
            if (resMesas.data.success) setMesas(resMesas.data.data);

            const resProd = await axios.get('http://localhost:5000/api/produtos', { withCredentials: true });
            if (resProd.data.success) {
                const grouped = { Bebida: [], Prato: [], Sobremesa: [] };
                resProd.data.data.forEach(p => { if (grouped[p.categoria]) grouped[p.categoria].push(p); });
                setProdutos(grouped);
            }
        } catch (error) { 
            console.error("Erro ao carregar dados", error);
            toast.error('Erro ao carregar mesas e produtos.');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const carregarComandas = async (numero_mesa) => {
        try {
            const res = await axios.get(`http://localhost:5000/api/salao/${numero_mesa}/comandas`, { withCredentials: true });
            if (res.data.success) {
                const ativas = res.data.data.filter(c => c.status !== 'Cancelado');
                setComandasMesa(ativas);
            }
        } catch (err) { console.error(err); }
    };

    const toggleMesa = async (numero) => {
        if (expandedMesa === numero) {
            setExpandedMesa(null);
            setSelectedComanda(null);
        } else {
            setSelectedComanda(null);
            await carregarComandas(numero);
            setExpandedMesa(numero);
        }
    };

    // ==========================================
    // METODOS DO CRUD DE MESAS (EXCLUSIVO ADMIN)
    // ==========================================
    const handleCriarMesa = async (e) => {
        e.preventDefault();
        if (!novaCapacidade || novaCapacidade <= 0) return toast.warning("Insira uma capacidade válida.");
        try {
            const res = await axios.post('http://localhost:5000/api/salao/criar', { capacidade: parseInt(novaCapacidade) }, { withCredentials: true });
            if (res.data.success) {
                toast.success("Mesa criada com sucesso!");
                setNovaCapacidade('');
                fetchData();
            } else { toast.error(res.data.message); }
        } catch (err) { toast.error("Erro ao criar mesa."); }
    };

    const handleDeletarMesa = async (e, numero_mesa) => {
        e.stopPropagation();
        if (!window.confirm(`Deseja realmente excluir a Mesa ${numero_mesa}?`)) return;
        try {
            const res = await axios.delete(`http://localhost:5000/api/salao/deletar/${numero_mesa}`, { withCredentials: true });
            if (res.data.success) {
                toast.success("Mesa excluída!");
                if (expandedMesa === numero_mesa) setExpandedMesa(null);
                fetchData();
            } else { toast.error(res.data.message); }
        } catch (err) { toast.error("Erro: Não é possível deletar uma mesa com comandas associadas."); }
    };

    const abrirEdicaoMesa = (e, mesa) => {
        e.stopPropagation();
        setEditingMesaNum(mesa.numero);
        const capacidadeAtual = mesa.capacidade.split('/')[1] || mesa.capacidade;
        setEditCapacidade(capacidadeAtual);
    };

    const handleSalvarEdicaoMesa = async (e, numero_mesa) => {
        e.preventDefault();
        try {
            const res = await axios.put(`http://localhost:5000/api/salao/editar/${numero_mesa}`, { capacidade: parseInt(editCapacidade) }, { withCredentials: true });
            if (res.data.success) {
                toast.success("Capacidade da mesa atualizada!");
                setEditingMesaNum(null);
                fetchData();
            } else { toast.error(res.data.message); }
        } catch (err) { toast.error("Erro ao editar mesa."); }
    };

    // ==========================================
    // OPERAÇÕES DE PEDIDOS E COMANDAS
    // ==========================================
    const criarNovaComanda = async (numero_mesa) => {
        try {
            const res = await axios.post(`http://localhost:5000/api/salao/${numero_mesa}/comandas/abrir_comanda`, {}, { withCredentials: true });
            if (res.data.success) {
                toast.success(`Comanda #${res.data.data.comanda_id} criada com sucesso!`);
                await carregarComandas(numero_mesa);
                setSelectedComanda(res.data.data.comanda_id);
                fetchData();
            }
        } catch (e) { toast.error("Erro ao criar nova comanda."); }
    };

    const adicionarAoCarrinho = (produto) => {
        if (!selectedComanda) return toast.warning("Selecione uma comanda na barra lateral primeiro!");
        setCart(prev => {
            const comandaCart = prev[selectedComanda] || [];
            const itemIndex = comandaCart.findIndex(i => i.product_id === produto.id);
            let novoCart;
            if (itemIndex >= 0) {
                novoCart = [...comandaCart];
                novoCart[itemIndex].quantidade += 1;
            } else {
                novoCart = [...comandaCart, { product_id: produto.id, nome: produto.nome, preco: produto.preco, quantidade: 1 }];
            }
            toast.success(`➕ ${produto.nome} adicionado.`);
            return { ...prev, [selectedComanda]: novoCart };
        });
    };

    const removerDoCarrinho = (comandaId, productId) => {
        setCart(prev => {
            const comandaCart = prev[comandaId] || [];
            return { ...prev, [comandaId]: comandaCart.filter(i => i.product_id !== productId) };
        });
    };

    const confirmarPedido = async (numero_mesa, comandaId) => {
        const itens = cart[comandaId];
        if (!itens || itens.length === 0) return;
        try {
            const promessas = itens.map(item => 
                axios.post(`http://localhost:5000/api/salao/${numero_mesa}/comandas/${comandaId}/adicionar_item`, {
                    product_id: item.product_id, quantidade: item.quantidade, observacao: ''
                }, { withCredentials: true })
            );
            await Promise.all(promessas);
            await axios.post(`http://localhost:5000/api/salao/${numero_mesa}/comandas/${comandaId}/enviar_comanda`, {}, { withCredentials: true });
            setCart(prev => ({ ...prev, [comandaId]: [] }));
            await carregarComandas(numero_mesa);
            toast.success(`🍽️ Pedido enviado à cozinha com sucesso!`);
        } catch (error) { toast.error("Erro ao confirmar o pedido."); }
    };

    const calcularTotalLocal = (comandaId) => {
        const itens = cart[comandaId] || [];
        return itens.reduce((acc, item) => acc + (item.preco * item.quantidade), 0);
    };

    const marcarComoEntregue = async (numero_mesa, comandaId) => {
        try {
            const res = await axios.put(`http://localhost:5000/api/salao/${numero_mesa}/comandas/${comandaId}/alterar_status`, 
                { status: 'Entregue' }, { withCredentials: true });
            if (res.data.success) {
                toast.success('Pedido marcado como Entregue.');
                await carregarComandas(numero_mesa);
                fetchData();
            } else {
                toast.error("Erro: " + res.data.message);
            }
        } catch (err) { toast.error("Erro ao marcar comanda como entregue."); }
    };

    // ==========================================
    // SISTEMA DE CAIXA E PAGAMENTO
    // ==========================================
    const calcularTotalDaConta = (comanda) => {
        const todosProdutos = [...produtos.Bebida, ...produtos.Prato, ...produtos.Sobremesa];
        return (comanda.itens || []).reduce((acc, item) => {
            const prod = todosProdutos.find(p => p.nome === item.produto);
            const preco = prod ? parseFloat(prod.preco) : 0;
            return acc + (preco * item.quantidade);
        }, 0);
    };

    const confirmarPagamento = async () => {
        try {
            const res = await axios.post(`http://localhost:5000/api/salao/${expandedMesa}/comandas/${modalConta.id}/fechar`, {}, { withCredentials: true });
            if (res.data.success) {
                toast.success(`✅ Pagamento via ${metodoPagamento} processado! Conta fechada.`);
                setModalConta(null);
                await carregarComandas(expandedMesa);
                if (selectedComanda === modalConta.id) setSelectedComanda(null);
                fetchData();
            } else {
                toast.error("Erro: " + res.data.message);
            }
        } catch(e) {
            toast.error("AVISO: Todos os pedidos dessa comanda devem constar como 'Entregue' para fechar a conta.");
        }
    };


    return (
        <SalaoLayout>
            <div className="pdv-container">
                <nav className="left-sidebar">
                    <div className="left-sidebar-header">Mesas</div>
                    
                    {cargo === 'ADMINISTRADOR' && (
                        <form onSubmit={handleCriarMesa} style={{ padding: '12px', borderBottom: '2px solid var(--border-color)', display: 'flex', gap: '8px' }}>
                            <div className="custom-number-input" style={{ flex: 1 }}>
                                <button type="button" className="spin-btn" onClick={() => setNovaCapacidade(prev => Math.max(1, (parseInt(prev) || 1) - 1))}>-</button>
                                <input 
                                    type="number" 
                                    placeholder="Cap" 
                                    value={novaCapacidade} 
                                    onChange={e => setNovaCapacidade(e.target.value)}
                                    min="1" required 
                                    style={{ flex: 1, width: '100%' }}
                                />
                                <button type="button" className="spin-btn" onClick={() => setNovaCapacidade(prev => (parseInt(prev) || 0) + 1)}>+</button>
                            </div>
                            <button type="submit" style={{ padding: '6px 12px', fontSize: '11px' }}>+ Criar</button>
                        </form>
                    )}

                    <ul className="mesas-list">
                        {isLoading ? (
                            Array.from({ length: 4 }).map((_, idx) => (
                                <li className="mesa-item skeleton" key={idx} style={{ height: '40px', marginBottom: '8px' }}></li>
                            ))
                        ) : (
                            mesas.map(mesa => {
                                const isExpanded = expandedMesa === mesa.numero;
                                const isEditing = editingMesaNum === mesa.numero;

                                return (
                                    <motion.li 
                                        className="mesa-item" 
                                        key={mesa.numero}
                                        initial={{ opacity: 0, x: -10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                    
                                    <div style={{ display: 'flex', alignItems: 'center', background: isExpanded ? '#2a0000' : 'transparent' }}>
                                        <button 
                                            className={`mesa-btn ${isExpanded ? 'active' : ''}`}
                                            onClick={() => toggleMesa(mesa.numero)}
                                            style={{ 
                                                flex: 1, background: 'transparent', border: 'none', textAlign: 'left',
                                                padding: '12px 10px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', minWidth: 0
                                            }}
                                        >
                                            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', whiteSpace: 'normal', lineHeight: '1.2' }}>
                                                <span style={{ fontSize: '12px', fontWeight: 'bold' }}>Mesa {mesa.numero} ({mesa.status})</span>
                                                <small style={{ color: '#aaa', fontSize: '10px' }}>Cap: {mesa.capacidade}</small>
                                            </div>
                                            <span style={{ marginLeft: '4px', fontSize: '10px' }}>{isExpanded ? '▼' : '▶'}</span>
                                        </button>
                                        
                                        {cargo === 'ADMINISTRADOR' && (
                                            <div style={{ display: 'flex', gap: '4px', paddingRight: '10px', flexShrink: 0 }}>
                                                <button onClick={(e) => abrirEdicaoMesa(e, mesa)} style={{ background: '#444', padding: '6px', fontSize: '10px', borderRadius: '4px' }}>✏️</button>
                                                <button onClick={(e) => handleDeletarMesa(e, mesa.numero)} className="danger" style={{ padding: '6px', fontSize: '10px', borderRadius: '4px' }}>✕</button>
                                            </div>
                                        )}
                                    </div>

                                    {isEditing && (
                                        <form onSubmit={(e) => handleSalvarEdicaoMesa(e, mesa.numero)} style={{ padding: '10px', background: '#221010', display: 'flex', gap: '6px', alignItems: 'center' }}>
                                            <label style={{ fontSize: '11px', color: '#ccc' }}>Nova Cap:</label>
                                            <div className="custom-number-input">
                                                <button type="button" className="spin-btn" onClick={() => setEditCapacidade(prev => Math.max(1, (parseInt(prev) || 1) - 1))}>-</button>
                                                <input 
                                                    type="number" 
                                                    value={editCapacidade} 
                                                    onChange={e => setEditCapacidade(e.target.value)}
                                                    min="1" required 
                                                />
                                                <button type="button" className="spin-btn" onClick={() => setEditCapacidade(prev => (parseInt(prev) || 0) + 1)}>+</button>
                                            </div>
                                            <button type="submit" style={{ padding: '4px 8px', fontSize: '10px', background: 'green' }}>Salvar</button>
                                        </form>
                                    )}
                                    
                                    <div className={`pedidos-panel ${isExpanded ? 'open' : ''}`}>
                                        <div className="pedidos-inner">
                                            {comandasMesa.map(comanda => {
                                                const isComandaActive = selectedComanda === comanda.id;
                                                const hasLocalItems = (cart[comanda.id] || []).length > 0;
                                                const totalStr = calcularTotalLocal(comanda.id).toFixed(2);

                                                return (
                                                    <div key={comanda.id} style={{
                                                        marginBottom: '10px', border: '1px solid #3a0000', borderRadius: '8px', padding: '10px',
                                                        background: isComandaActive ? '#2a0000' : '#111'
                                                    }}>
                                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer', marginBottom: '8px' }} onClick={() => setSelectedComanda(comanda.id)}>
                                                            <strong style={{ color: isComandaActive ? '#ff6666' : '#ccc' }}>Cmd #{comanda.id}</strong>
                                                            <span style={{ fontSize: '10px', background: '#440000', padding: '3px 6px', borderRadius: '4px' }}>{comanda.status}</span>
                                                        </div>
                                                        
                                                        {isComandaActive && (
                                                            <div>
                                                                {hasLocalItems ? (
                                                                    <>
                                                                        {(cart[comanda.id] || []).map(item => (
                                                                            <div className="pedido-item" key={item.product_id} style={{ borderBottom: 'none' }}>
                                                                                <span>{item.quantidade}x {item.nome}</span>
                                                                                <div style={{ display: 'flex', alignItems: 'center' }}>
                                                                                    <span style={{ color: '#ff6666' }}>R$ {(item.preco * item.quantidade).toFixed(2)}</span>
                                                                                    <button onClick={() => removerDoCarrinho(comanda.id, item.product_id)} style={{ background:'none', border:'none', color:'#888', marginLeft:'10px', cursor:'pointer' }}>✕</button>
                                                                                </div>
                                                                            </div>
                                                                        ))}
                                                                        <div style={{ marginTop: '5px', display: 'flex', justifyContent: 'space-between', fontWeight: 'bold' }}>
                                                                            <span>Total:</span>
                                                                            <span style={{ color: 'var(--primary-red)' }}>R$ {totalStr}</span>
                                                                        </div>
                                                                        <button onClick={() => confirmarPedido(mesa.numero, comanda.id)} style={{ width: '100%', marginTop: '10px', fontSize: '10px' }}>✔ Enviar Novo Pedido</button>
                                                                    </>
                                                                ) : (
                                                                    <p style={{ textAlign: 'center', color: '#555', fontStyle: 'italic', fontSize: '11px', margin: '10px 0' }}>Selecione produtos ao lado</p>
                                                                )}
                                                                {/* NOVO BOTÃO DE ENTREGUE (Só aparece se a cozinha marcou como Pronto) */}
                                                                {comanda.status === 'Pronto' && (
                                                                    <button onClick={() => marcarComoEntregue(mesa.numero, comanda.id)} style={{ width: '100%', marginTop: '8px', fontSize: '10px', background: 'linear-gradient(90deg, #cc7700, #ffaa00)', color: '#111', fontWeight: 'bold' }}>
                                                                        🍽️ Marcar como Entregue
                                                                    </button>
                                                                )}
                                                                
                                                                {/* BOTÃO DE CHECKOUT QUE ABRE O MODAL */}
                                                                <button onClick={() => setModalConta(comanda)} className="danger" style={{ width: '100%', marginTop: '8px', fontSize: '10px' }}>
                                                                    🧾 Ver Conta e Pagar
                                                                </button>
                                                            </div>
                                                        )}
                                                    </div>
                                                );
                                            })}

                                            <button onClick={() => criarNovaComanda(mesa.numero)} style={{ width: '100%', marginTop: '5px', background: '#222', color: '#ccc', border: '1px dashed #555' }}>
                                                + Abrir Nova Comanda
                                            </button>
                                        </div>
                                    </div>
                                    </motion.li>
                                );
                            })
                        )}
                    </ul>
                </nav>

                <div className="menu-area">
                    {!selectedComanda ? (
                        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666', flexDirection: 'column' }}>
                            <span style={{ fontSize: '40px', opacity: 0.5 }}>🍽️</span>
                            <p style={{ marginTop: '10px' }}>Selecione ou crie uma comanda na barra lateral.</p>
                        </div>
                    ) : (
                        <>
                            <div style={{ background: '#2a0000', color: '#fff', textAlign: 'center', padding: '8px', fontSize: '12px' }}>
                                Adicionando itens na <strong>Comanda #{selectedComanda} (Mesa {expandedMesa})</strong>
                            </div>
                            
                            <nav className="menu-header-nav">
                                {Object.keys(produtos).map(cat => (
                                    <button key={cat} className={`menu-tab ${activeTab === cat ? 'active' : ''}`} onClick={() => setActiveTab(cat)}>
                                        {cat}s
                                    </button>
                                ))}
                            </nav>

                            <div className="products-grid">
                                {produtos[activeTab].map(prod => (
                                    <motion.div 
                                        className="product-card" 
                                        key={prod.id} 
                                        onClick={() => adicionarAoCarrinho(prod)}
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                    >
                                        <div style={{ fontSize: '40px', color: '#ccc', marginBottom: '10px' }}>📦</div>
                                        <div className="product-name">{prod.nome}</div>
                                        <div className="product-price">R$ {parseFloat(prod.preco).toFixed(2)}</div>
                                    </motion.div>
                                ))}
                            </div>
                        </>
                    )}
                </div>
            </div>

            {/* ==========================================
                MODAL FLUTUANTE DE PAGAMENTO DA CONTA 
            ========================================== */}
            {modalConta && (
                <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.85)', zIndex: 9999, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <div className="card" style={{ width: '380px', background: '#111', border: '1px solid #cc0000', boxShadow: '0 10px 30px rgba(200,0,0,0.2)' }}>
                        <h2 style={{ textAlign: 'center', color: '#fff', borderBottom: '1px solid #333', paddingBottom: '15px', marginBottom: '15px' }}>
                            Conta - Comanda #{modalConta.id}
                        </h2>
                        
                        <div style={{ maxHeight: '250px', overflowY: 'auto', marginBottom: '20px', paddingRight: '10px' }}>
                            {(modalConta.itens || []).length === 0 ? (
                                <p style={{ textAlign: 'center', color: '#555', fontStyle: 'italic' }}>Nenhum item consumido.</p>
                            ) : (
                                (modalConta.itens || []).map((item, idx) => {
                                    const todos = [...produtos.Bebida, ...produtos.Prato, ...produtos.Sobremesa];
                                    const prod = todos.find(p => p.nome === item.produto);
                                    const preco = prod ? parseFloat(prod.preco) : 0;
                                    return (
                                        <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #222', padding: '8px 0', fontSize: '13px' }}>
                                            <span style={{ color: '#ccc' }}>{item.quantidade}x {item.produto}</span>
                                            <span style={{ color: '#fff' }}>R$ {(preco * item.quantidade).toFixed(2)}</span>
                                        </div>
                                    );
                                })
                            )}
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#2a0000', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>
                            <span style={{ fontSize: '14px', fontWeight: 'bold', color: '#ffaaaa' }}>TOTAL A PAGAR</span>
                            <span style={{ fontSize: '20px', fontWeight: 'bold', color: '#fff' }}>R$ {calcularTotalDaConta(modalConta).toFixed(2)}</span>
                        </div>

                        <div style={{ marginBottom: '20px' }}>
                            <label style={{ fontSize: '11px', color: '#888', display: 'block', marginBottom: '5px' }}>Forma de Pagamento:</label>
                            <select value={metodoPagamento} onChange={e => setMetodoPagamento(e.target.value)} style={{ width: '100%', padding: '10px' }}>
                                <option value="PIX">PIX</option>
                                <option value="Cartão de Crédito">Cartão de Crédito</option>
                                <option value="Cartão de Débito">Cartão de Débito</option>
                                <option value="Dinheiro">Dinheiro</option>
                            </select>
                        </div>

                        <div style={{ display: 'flex', gap: '10px' }}>
                            <button onClick={() => setModalConta(null)} style={{ flex: 1, background: '#333', color: '#ccc' }}>Cancelar</button>
                            <button onClick={confirmarPagamento} style={{ flex: 1, background: 'linear-gradient(90deg, #004a00, #008b00)' }}>✔ Confirmar Pagamento</button>
                        </div>
                    </div>
                </div>
            )}
        </SalaoLayout>
    );
}