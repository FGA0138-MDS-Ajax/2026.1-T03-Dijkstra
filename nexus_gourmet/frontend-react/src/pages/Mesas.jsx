import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';
import SalaoLayout from '../components/SalaoLayout';
import ConfirmDialog from '../components/ConfirmDialog';
import EmptyState from '../components/EmptyState';

export default function Mesas() {
    const [mesas, setMesas] = useState([]);
    const [produtos, setProdutos] = useState({ Bebida: [], Prato: [], Sobremesa: [] });
    const [isLoading, setIsLoading] = useState(true);
    const cargo = localStorage.getItem('userCargo');
    
    // Estados da Interface de Comandas
    const [expandedMesa, setExpandedMesa] = useState(null);
    const [comandasMesa, setComandasMesa] = useState([]);
    const [selectedComanda, setSelectedComanda] = useState(null);
    const [activeTab, setActiveTab] = useState('Todos');

    // Controle da gaveta (drawer) de mesas no mobile — no desktop essa
    // classe/estado simplesmente não tem efeito nenhum (é ignorado pelo CSS)
    const [sidebarOpen, setSidebarOpen] = useState(false);

    // Estados de Busca
    const [searchMesa, setSearchMesa] = useState('');
    const [searchProduto, setSearchProduto] = useState('');
    
    // Estados do CRUD de Mesas (Admin)
    const [novaCapacidade, setNovaCapacidade] = useState('');
    const [editingMesaNum, setEditingMesaNum] = useState(null);
    const [editCapacidade, setEditCapacidade] = useState('');

    // Estados do Modal de Pagamento (Caixa)
    const [modalConta, setModalConta] = useState(null);
    const [metodoPagamento, setMetodoPagamento] = useState('PIX');

    const [comandaParaCancelar, setComandaParaCancelar] = useState(null);

    // Carrinho local por Comanda
    const [cart, setCart] = useState({});

    // Estados dos Modais de Confirmação (Prevenção de Erros)
    const [mesaParaDeletar, setMesaParaDeletar] = useState(null);
    const [itemParaRemover, setItemParaRemover] = useState(null); // { comandaId, product_id, nome, quantidade }
    const [comandaParaEnviar, setComandaParaEnviar] = useState(null); // { numero_mesa, comandaId }
    const [contaParaFechar, setContaParaFechar] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);

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

    // Assim que o usuário escolhe uma comanda, fecha a gaveta de mesas
    // (no desktop isso não muda nada visualmente, o CSS ignora)
    useEffect(() => {
        if (selectedComanda) setSidebarOpen(false);
    }, [selectedComanda]);

    const carregarComandas = async (numero_mesa) => {
    try {
        const res = await axios.get(`http://localhost:5000/api/salao/${numero_mesa}/comandas`, { withCredentials: true });
        
        // Se o back-end retornou sucesso mas a lista está vazia (pós-fechamento), 
        // o front-end atualizará o estado para [] e as comandas sumirão da tela
        if (res.data.success) {
            const ativas = res.data.data.filter(c => !['Cancelado', 'Finalizado'].includes(c.status));
            setComandasMesa(ativas); // Isso vai limpar a tela se 'ativas' for []
        }
    } catch (err) { 
        setComandasMesa([]); // Garante que, em caso de erro ou expiração, nada seja mostrado
        console.error(err); 
    }
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
            const res = await axios.post('http://localhost:5000/api/salao/criar_mesa', { capacidade: parseInt(novaCapacidade) }, { withCredentials: true });
            if (res.data.success) {
                toast.success("Mesa criada com sucesso!");
                setNovaCapacidade('');
                fetchData();
            } else { toast.error(res.data.message); }
        } catch (err) { toast.error("Erro ao criar mesa."); }
    };

    const handleDeletarMesa = (e, numero_mesa) => {
        e.stopPropagation();
        setMesaParaDeletar(numero_mesa);
    };

    const confirmarDelecaoMesa = async () => {
        if (!mesaParaDeletar) return;
        setIsProcessing(true);
        try {
            const res = await axios.delete(`http://localhost:5000/api/salao/deletar_mesa/${mesaParaDeletar}`, { withCredentials: true });
            if (res.data.success) {
                toast.success("Mesa excluída!");
                if (expandedMesa === mesaParaDeletar) setExpandedMesa(null);
                fetchData();
                setMesaParaDeletar(null);
            } else { toast.error(res.data.message); }
        } catch (err) { 
            toast.error("Erro: Não é possível deletar uma mesa com comandas associadas."); 
        } finally {
            setIsProcessing(false);
        }
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
            const res = await axios.put(`http://localhost:5000/api/salao/editar_mesa/${numero_mesa}`, { capacidade: parseInt(editCapacidade) }, { withCredentials: true });
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

    const prepararRemocaoItem = (comandaId, item) => {
        setItemParaRemover({ comandaId, ...item });
    };

    const confirmarCancelamentoComanda = async () => {
    if (!comandaParaCancelar) return;
    setIsProcessing(true);
    try {
        // Utilizamos a rota de editar_comanda enviando o comando de cancelar
        const res = await axios.put(`http://localhost:5000/api/salao/${expandedMesa}/comandas/${comandaParaCancelar}/editar_comanda`, 
            { cancelar: true }, 
            { withCredentials: true }
        );

        if (res.data.success) {
            toast.success('❌ Comanda cancelada com sucesso.');
            setComandaParaCancelar(null);
            await carregarComandas(expandedMesa);
            if (selectedComanda === comandaParaCancelar) setSelectedComanda(null);
            fetchData();
        } else {
            toast.error("Erro: " + res.data.message);
        }
    } catch (err) {
        toast.error("Erro ao cancelar comanda.");
    } finally {
        setIsProcessing(false);
    }
};

    const confirmarRemocaoItem = () => {
        if (!itemParaRemover) return;
        setCart(prev => {
            const comandaCart = prev[itemParaRemover.comandaId] || [];
            return { ...prev, [itemParaRemover.comandaId]: comandaCart.filter(i => i.product_id !== itemParaRemover.product_id) };
        });
        toast.success(`🗑️ Item removido da comanda.`);
        setItemParaRemover(null);
    };

    const prepararEnvioComanda = (numero_mesa, comandaId) => {
        const itens = cart[comandaId] || [];
        if (itens.length === 0) {
            return toast.warning("Adicione pelo menos um item antes de enviar a comanda para a cozinha.");
        }
        setComandaParaEnviar({ numero_mesa, comandaId });
    };

    const confirmarEnvioComanda = async () => {
        if (!comandaParaEnviar) return;
        setIsProcessing(true);
        const { numero_mesa, comandaId } = comandaParaEnviar;
        const itens = cart[comandaId];
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
            setComandaParaEnviar(null);
        } catch (error) { 
            toast.error("Erro ao confirmar o pedido."); 
        } finally {
            setIsProcessing(false);
        }
    };

    const calcularTotalLocal = (comandaId) => {
        const itens = cart[comandaId] || [];
        return itens.reduce((acc, item) => acc + (item.preco * item.quantidade), 0);
    };

    const marcarComoEntregue = async (numero_mesa, comandaId) => {
        try {
            const res = await axios.put(`http://localhost:5000/api/cozinha/${comandaId}/alterar_status`, { status: 'Entregue' }, { withCredentials: true });
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

    const prepararFechamentoConta = () => {
        setContaParaFechar(modalConta);
    };

    const confirmarFechamentoConta = async () => {
        if (!contaParaFechar) return;
        setIsProcessing(true);
        try {
            const res = await axios.post(`http://localhost:5000/api/salao/${expandedMesa}/comandas/${contaParaFechar.id}/fechar_comanda`, {}, { withCredentials: true });
            if (res.data.success) {
                toast.success(`✅ Pagamento via ${metodoPagamento} processado! Conta fechada.`);
                setModalConta(null);
                setContaParaFechar(null);
                await carregarComandas(expandedMesa);
                if (selectedComanda === contaParaFechar.id) setSelectedComanda(null);
                fetchData();
            } else {
                toast.error("Erro: " + res.data.message);
            }
        } catch(e) {
            toast.error("AVISO: Todos os pedidos dessa comanda devem constar como 'Entregue' para fechar a conta.");
        } finally {
            setIsProcessing(false);
        }
    };


    const filteredMesas = mesas.filter(m => m.numero.toString().includes(searchMesa) || (m.identificacao && m.identificacao.toLowerCase().includes(searchMesa.toLowerCase())));

    const getFilteredProdutos = () => {
        let allProds = [];
        if (activeTab === 'Todos') {
            allProds = [...produtos.Bebida, ...produtos.Prato, ...produtos.Sobremesa];
        } else {
            allProds = produtos[activeTab] || [];
        }
        return allProds.filter(p => p.nome.toLowerCase().includes(searchProduto.toLowerCase()));
    };
    const filteredProdutosParaComanda = getFilteredProdutos();

    return (
        <SalaoLayout>
            <div className="pdv-container">
                <nav className={`left-sidebar ${sidebarOpen ? 'open' : ''}`}>
                    <div className="left-sidebar-header">
                        <svg viewBox="0 0 24 24" fill="none" stroke="#cc0000" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" width="20" height="20">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <line x1="3" y1="9" x2="21" y2="9"></line>
                            <line x1="9" y1="21" x2="9" y2="9"></line>
                        </svg>
                        <span>Controle de Mesas</span>
                    </div>
                    
                    <div style={{ padding: '10px', borderBottom: '1px solid var(--border)' }}>
                        <div className="search-container" style={{ marginBottom: 0 }}>
                            <span className="search-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="16" height="16">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                </svg>
                            </span>
                            <input 
                                 type="text" 
                                 className="search-input" 
                                 placeholder="Buscar mesa..." 
                                 value={searchMesa}
                                onChange={e => setSearchMesa(e.target.value)}
                            />
                        </div>
                    </div>

                    {cargo === 'ADMINISTRADOR' && (
                        <form onSubmit={handleCriarMesa} className="add-table-form">
                            <div className="table-input-group">
                                <span className="input-label-hint">Capacidade</span>
                                <div className="modern-number-input">
                                    <button 
                                        type="button" 
                                        className="spin-btn minus" 
                                        onClick={() => setNovaCapacidade(prev => Math.max(1, (parseInt(prev) || 1) - 1))}
                                    >
                                        −
                                    </button>
                                    <input 
                                        type="number"
                                        placeholder="0"
                                        value={novaCapacidade}
                                        onChange={e => setNovaCapacidade(e.target.value)}
                                        min="1" 
                                        required 
                                    />
                                    <button 
                                        type="button" 
                                        className="spin-btn plus" 
                                        onClick={() => setNovaCapacidade(prev => (parseInt(prev) || 0) + 1)}
                                    >
                                        +
                                    </button>
                                </div>
                            </div>
                            <button type="submit" className="btn-create-table">
                                <span>+ Criar Mesa</span>
                            </button>
                        </form>
                    )}

                    <ul className="mesas-list">
                        {isLoading ? (
                            Array.from({ length: 4 }).map((_, idx) => (
                                <li className="mesa-item skeleton" key={idx} style={{ height: '40px', marginBottom: '8px' }}></li>
                            ))
                        ) : filteredMesas.length === 0 ? (
                            <div style={{ padding: '10px' }}>
                                <EmptyState icon="🍽️" title="Nenhuma mesa" />
                            </div>
                        ) : (
                            filteredMesas.map(mesa => {
                                const isExpanded = expandedMesa === mesa.numero;
                                const isEditing = editingMesaNum === mesa.numero;
                                  
                                const getStatusColor = (status) => {
                                    if (status === 'Livre') return '#00cc66'; // Verde
                                    if (status === 'Ocupada') return '#ff3333'; // Vermelho
                                    return '#ffaa00'; // Laranja para outros status
                                };
                                const statusColor = getStatusColor(mesa.status);

                                return (
                                    <motion.li 
                                        className="mesa-item" 
                                        key={mesa.numero}
                                        initial={{ opacity: 0, x: -10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                    
                                    <div style={{
                                            display: 'flex',
                                            alignItems: 'center',
                                            background: isExpanded ? '#1a0000' : 'transparent',
                                            borderLeft: isExpanded ? '4px solid #cc0000' : '4px solid transparent',
                                            transition: 'all 0.2s ease',
                                            overflow: 'hidden' /* Evita qualquer vazamento */
                                        }}>
                                            <button
                                                className={`mesa-btn ${isExpanded ? 'active' : ''}`}
                                                onClick={() => toggleMesa(mesa.numero)}
                                                style={{
                                                    flex: 1, 
                                                    background: 'transparent', 
                                                    border: 'none', 
                                                    textAlign: 'left',
                                                    padding: '10px', /* Reduzido para dar mais espaço */
                                                    display: 'flex', 
                                                    alignItems: 'center', 
                                                    minWidth: 0, 
                                                    width: 'auto' /* Sobrescreve o width 100% que causava o bug */
                                                }}
                                            >
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', minWidth: 0 }}>
                                                    {/* Bloco com o Número da Mesa */}
                                                    <div style={{
                                                        width: '36px',
                                                        height: '36px',
                                                        flexShrink: 0,
                                                        borderRadius: '8px',
                                                        background: isExpanded ? 'linear-gradient(135deg, #cc0000, #8b0000)' : '#1a1a1a',
                                                        border: `1px solid ${isExpanded ? '#ff3333' : '#333'}`,
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        justifyContent: 'center',
                                                        fontSize: '15px',
                                                        fontWeight: '900',
                                                        color: isExpanded ? '#fff' : '#ccc',
                                                        boxShadow: isExpanded ? '0 4px 10px rgba(204,0,0,0.3)' : 'none',
                                                        transition: 'all 0.3s ease'
                                                    }}>
                                                        {mesa.numero}
                                                    </div>

                                                    {/* Informações da Mesa */}
                                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', minWidth: 0 }}>
                                                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                                            <span style={{ fontSize: '13px', fontWeight: '800', color: isExpanded ? '#fff' : '#ddd', letterSpacing: '1px' }}>
                                                                MESA
                                                            </span>
                                                            <span style={{
                                                                fontSize: '9px',
                                                                padding: '2px 6px',
                                                                borderRadius: '10px',
                                                                background: `${statusColor}22`,
                                                                color: statusColor,
                                                                border: `1px solid ${statusColor}55`,
                                                                fontWeight: 'bold',
                                                                textTransform: 'uppercase',
                                                                letterSpacing: '0.5px',
                                                                whiteSpace: 'nowrap'
                                                            }}>
                                                                {mesa.status}
                                                            </span>
                                                        </div>
                                                        <span style={{ color: '#888', fontSize: '11px', fontWeight: '500', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                                            Cap: {mesa.capacidade}
                                                        </span>
                                                    </div>
                                                </div>
                                            </button>

                                            {/* BOTOES DE ADMIN (EDITAR E DELETAR) */}
                                            {cargo === 'ADMINISTRADOR' && (
                                                <div style={{ display: 'flex', gap: '6px', paddingRight: '10px', flexShrink: 0 }}>
                                                    <button 
                                                        onClick={(e) => abrirEdicaoMesa(e, mesa)} 
                                                        style={{ 
                                                            background: isEditing ? '#cc0000' : '#222', 
                                                            color: '#fff', 
                                                            padding: '6px', /* Botões um pouco menores */
                                                            border: '1px solid #444', 
                                                            borderRadius: '6px', 
                                                            display: 'flex', 
                                                            alignItems: 'center', 
                                                            justifyContent: 'center', 
                                                            transition: 'all 0.2s' 
                                                        }} 
                                                        title="Editar Capacidade"
                                                    >
                                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="14" height="14"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                                                    </button>
                                                    <button 
                                                        onClick={(e) => handleDeletarMesa(e, mesa.numero)} 
                                                        className="danger" 
                                                        style={{ 
                                                            padding: '6px', 
                                                            borderRadius: '6px', 
                                                            display: 'flex', 
                                                            alignItems: 'center', 
                                                            justifyContent: 'center' 
                                                        }} 
                                                        title="Excluir Mesa"
                                                    >
                                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="14" height="14"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                                                    </button>
                                                </div>
                                            )}
                                        </div>

                                        {/* FORMULÁRIO DE EDIÇÃO CORRIGIDO E OTIMIZADO */}
                                        {isEditing && (
                                            <form onSubmit={(e) => handleSalvarEdicaoMesa(e, mesa.numero)} style={{ 
                                                padding: '12px', 
                                                background: '#150000', 
                                                borderBottom: '1px solid #333', 
                                                display: 'flex', 
                                                flexDirection: 'column', 
                                                gap: '12px' 
                                            }}>
                                                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                                    <label style={{ 
                                                        fontSize: '10px', 
                                                        color: '#ff8888', 
                                                        fontWeight: 'bold', 
                                                        textTransform: 'uppercase', 
                                                        letterSpacing: '0.5px' 
                                                    }}>
                                                        Nova Cap:
                                                    </label>
                                                    <div className="modern-number-input" style={{ width: '100px', height: '32px' }}>
                                                        <button type="button" className="spin-btn minus" onClick={() => setEditCapacidade(prev => Math.max(1, (parseInt(prev) || 1) - 1))}>-</button>
                                                        <input type="number" value={editCapacidade} onChange={e => setEditCapacidade(e.target.value)} min="1" required style={{ fontSize: '13px', padding: '0', textAlign: 'center' }} />
                                                        <button type="button" className="spin-btn plus" onClick={() => setEditCapacidade(prev => (parseInt(prev) || 0) + 1)}>+</button>
                                                    </div>
                                                </div>
                                                <div style={{ display: 'flex', gap: '8px' }}>
                                                    <button type="button" onClick={() => setEditingMesaNum(null)} style={{ 
                                                        flex: 1, 
                                                        background: 'transparent', 
                                                        color: '#ccc', 
                                                        border: '1px solid #444', 
                                                        padding: '8px', 
                                                        fontSize: '11px',
                                                        borderRadius: '6px',
                                                        fontWeight: 'bold',
                                                        cursor: 'pointer'
                                                    }}>
                                                        Cancelar
                                                    </button>
                                                    <button type="submit" style={{ 
                                                        flex: 1, 
                                                        background: '#00cc66', 
                                                        color: '#fff', 
                                                        border: 'none', 
                                                        padding: '8px', 
                                                        fontSize: '11px',
                                                        borderRadius: '6px',
                                                        fontWeight: 'bold',
                                                        cursor: 'pointer',
                                                        boxShadow: '0 2px 8px rgba(0,204,102,0.3)'
                                                    }}>
                                                        Salvar
                                                    </button>
                                                </div>
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
                                                    <div style={{
                                                         display: 'flex',
                                                         justifyContent: 'space-between',
                                                         alignItems: 'center',
                                                         cursor: 'pointer',
                                                         marginBottom: '12px',
                                                         paddingBottom: '10px',
                                                         borderBottom: isComandaActive ? '1px solid #cc0000' : '1px solid #333'
                                                     }} onClick={() => setSelectedComanda(comanda.id)}>
                                                         <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                                             <span style={{
                                                                 background: isComandaActive ? 'linear-gradient(90deg, #cc0000, #ff3333)' : '#333',
                                                                 color: '#fff',
                                                                 padding: '4px 8px',
                                                                 borderRadius: '6px',
                                                                 fontSize: '12px',
                                                                 fontWeight: '900',
                                                                 boxShadow: isComandaActive ? '0 2px 8px rgba(204,0,0,0.4)' : 'none'
                                                             }}>
                                                                 #{comanda.id}
                                                             </span>
                                                             <strong style={{
                                                                 color: isComandaActive ? '#fff' : '#888',
                                                                 fontSize: '14px',
                                                                 letterSpacing: '0.5px'
                                                             }}>Comanda</strong>
                                                         </div>
                                                         <span style={{
                                                             fontSize: '10px',
                                                             background: isComandaActive ? 'rgba(204,0,0,0.15)' : '#222',
                                                             color: isComandaActive ? '#ff6666' : '#777',
                                                             padding: '4px 10px',
                                                             borderRadius: '12px',
                                                             fontWeight: 'bold',
                                                             textTransform: 'uppercase',
                                                             letterSpacing: '1px',
                                                             border: isComandaActive ? '1px solid rgba(204,0,0,0.3)' : '1px solid #333'
                                                         }}>
                                                             {comanda.status}
                                                         </span>
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
                                                                                    <button onClick={() => prepararRemocaoItem(comanda.id, item)} style={{ background:'none', border:'none', color:'#888', marginLeft:'10px', cursor:'pointer' }}>✕</button>
                                                                                </div>
                                                                            </div>
                                                                        ))}
                                                                        <div style={{ marginTop: '5px', display: 'flex', justifyContent: 'space-between', fontWeight: 'bold' }}>
                                                                            <span>Total:</span>
                                                                            <span style={{ color: 'var(--primary-red)' }}>R$ {totalStr}</span>
                                                                        </div>
                                                                        <button onClick={() => prepararEnvioComanda(mesa.numero, comanda.id)} style={{ width: '100%', marginTop: '10px', fontSize: '10px' }}>✔ Enviar Novo Pedido</button>
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
                                                                
                                                                {/* BOTÃO DE CHECKOUT QUE ABRE O MODAL - SÓ MOSTRA SE ENTREGUE */}
                                                                {comanda.status === 'Entregue' && (
                                                                    <button onClick={() => setModalConta(comanda)} className="danger" style={{ width: '100%', marginTop: '8px', fontSize: '10px' }}>
                                                                        🧾 Ver Conta e Pagar
                                                                    </button>
                                                                )}
                                                                {/* O SEU NOVO BOTÃO DEVE ESTAR AQUI, DENTRO DA MESMA DIV */}
                                                                {(comanda.status === 'Pendente' || comanda.status === 'Em Preparo') && (
                                                                    <button 
                                                                        onClick={() => setComandaParaCancelar(comanda.id)} 
                                                                        style={{ width: '100%', marginTop: '8px', fontSize: '10px', background: '#333', color: '#ff6666', border: '1px solid #550000' }}
                                                                    >
                                                                        ❌ Cancelar Comanda
                                                                    </button>
                                                                )}
                                                            </div>
                                                        )}
                                                    </div>
                                                );
                                            })}

                                            <motion.button
                                                 whileHover={{ scale: 1.02, backgroundColor: 'rgba(204, 0, 0, 0.15)' }}
                                                 whileTap={{ scale: 0.98 }}
                                                 onClick={() => criarNovaComanda(mesa.numero)}
                                                 style={{
                                                     width: '100%',
                                                     marginTop: '12px',
                                                     padding: '14px',
                                                     background: 'rgba(204, 0, 0, 0.05)',
                                                     color: '#ff6666',
                                                     border: '1px dashed #cc0000',
                                                     borderRadius: '8px',
                                                     fontWeight: 'bold',
                                                     textTransform: 'uppercase',
                                                     letterSpacing: '1px',
                                                     cursor: 'pointer',
                                                     display: 'flex',
                                                     justifyContent: 'center',
                                                     alignItems: 'center',
                                                     gap: '8px',
                                                     transition: 'background-color 0.3s ease'
                                                 }}>
                                                 <span style={{ fontSize: '18px', fontWeight: '900', lineHeight: '1' }}>+</span> 
                                                 Abrir Nova Comanda
                                             </motion.button>
                                        </div>
                                    </div>
                                    </motion.li>
                                );
                            })
                        )}
                    </ul>
                </nav>

                {sidebarOpen && (
                    <div className="sidebar-backdrop" onClick={() => setSidebarOpen(false)} />
                )}

                <div className="menu-area">
                    <button
                        type="button"
                        className="mobile-sidebar-toggle"
                        onClick={() => setSidebarOpen(prev => !prev)}
                    >
                        {sidebarOpen
                            ? '✕ Fechar'
                            : `☰ ${expandedMesa ? `Mesa ${expandedMesa}` : 'Ver Mesas'}`}
                    </button>

                    {!selectedComanda ? (
                        <div className="menu-empty-state">
                            <span className="menu-empty-state__icon">🍽️</span>
                            <p className="menu-empty-state__text">Selecione ou crie uma comanda na barra lateral.</p>
                        </div>
                    ) : (
                        <>
                            <div style={{ background: '#2a0000', color: '#fff', textAlign: 'center', padding: '8px', fontSize: '12px' }}>
                                Adicionando itens na <strong>Comanda #{selectedComanda} (Mesa {expandedMesa})</strong>
                            </div>
                            
                            <div className="category-pills" style={{ padding: '0 10px', marginTop: '10px', marginBottom: '10px' }}>
                                {['Todos', 'Bebida', 'Prato', 'Sobremesa'].map(cat => (
                                    <button 
                                        key={cat} 
                                        className={`category-pill ${activeTab === cat ? 'active' : ''}`} 
                                        onClick={() => setActiveTab(cat)}
                                    >
                                        {cat}
                                    </button>
                                ))}
                            </div>
                            
                            <div style={{ padding: '0 10px', marginBottom: '10px' }}>
                                <div className="search-container" style={{ marginBottom: 0 }}>
                                    <span className="search-icon">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="16" height="16">
                                            <circle cx="11" cy="11" r="8"></circle>
                                            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                        </svg>
                                    </span>
                                    <input 
                                         type="text" 
                                         className="search-input" 
                                         placeholder="Buscar produto para adicionar..." 
                                         value={searchProduto}
                                        onChange={e => setSearchProduto(e.target.value)}
                                    />
                                </div>
                            </div>

                            {filteredProdutosParaComanda.length === 0 ? (
                                <div style={{ padding: '20px' }}>
                                    <EmptyState icon="📦" title="Nenhum produto encontrado" description="Tente alterar a categoria ou o termo da busca." />
                                </div>
                            ) : (
                                <div className="products-grid">
                                    {filteredProdutosParaComanda.map(prod => (
                                        <motion.div 
                                            className="product-card" 
                                            key={prod.id} 
                                            onClick={() => adicionarAoCarrinho(prod)}
                                            whileHover={{ scale: 1.05 }}
                                            whileTap={{ scale: 0.95 }}
                                        >
                                            {prod.foto_produto ? (
                                                <img src={`http://localhost:5000${prod.foto_produto}`} alt={prod.nome} style={{ width: '100%', height: '80px', objectFit: 'cover', borderRadius: '8px', marginBottom: '8px' }} />
                                            ) : (
                                                <div style={{ fontSize: '40px', color: '#ccc', marginBottom: '10px' }}>📦</div>
                                            )}
                                            <div className="product-name">{prod.nome}</div>
                                            <div className="product-price">R$ {parseFloat(prod.preco).toFixed(2)}</div>
                                        </motion.div>
                                    ))}
                                </div>
                            )}
                        </>
                    )}
                </div>
            </div>

            {/* ==========================================
                MODAL FLUTUANTE DE PAGAMENTO DA CONTA 
            ========================================== */}
            {modalConta && (
                <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.85)', zIndex: 9999, display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '16px', boxSizing: 'border-box' }}>
                    <div className="card" style={{ width: '90vw', maxWidth: '380px', maxHeight: '90vh', overflowY: 'auto', background: '#111', border: '1px solid #cc0000', boxShadow: '0 10px 30px rgba(200,0,0,0.2)' }}>
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
                            <button onClick={prepararFechamentoConta} style={{ flex: 1, background: 'linear-gradient(90deg, #004a00, #008b00)' }}>✔ Confirmar Pagamento</button>
                        </div>
                    </div>
                </div>
            )}

            {/* Modais de Confirmação Inteligentes */}
            <ConfirmDialog 
                isOpen={!!mesaParaDeletar}
                title="Excluir Mesa?"
                description={`Esta ação removerá a Mesa ${mesaParaDeletar} do salão. Você tem certeza?`}
                confirmLabel="Excluir mesa"
                cancelLabel="Cancelar"
                variant="danger"
                isLoading={isProcessing}
                onConfirm={confirmarDelecaoMesa}
                onCancel={() => setMesaParaDeletar(null)}
            />

            <ConfirmDialog 
                isOpen={!!itemParaRemover}
                title="Remover item da comanda?"
                description={`Você está prestes a remover: ${itemParaRemover?.quantidade}x ${itemParaRemover?.nome}`}
                confirmLabel="Remover item"
                cancelLabel="Manter item"
                variant="warning"
                isLoading={isProcessing}
                onConfirm={confirmarRemocaoItem}
                onCancel={() => setItemParaRemover(null)}
            />

            <ConfirmDialog 
                isOpen={!!comandaParaEnviar}
                title="Enviar comanda para cozinha?"
                description={`Após enviar, a cozinha receberá o pedido imediatamente. Confirma o envio de ${comandaParaEnviar ? cart[comandaParaEnviar.comandaId]?.length : 0} item(s)?`}
                confirmLabel="Enviar para cozinha"
                cancelLabel="Revisar pedido"
                variant="primary"
                isLoading={isProcessing}
                onConfirm={confirmarEnvioComanda}
                onCancel={() => setComandaParaEnviar(null)}
            >
                {comandaParaEnviar && cart[comandaParaEnviar.comandaId] && (
                    <div style={{ maxHeight: '150px', overflowY: 'auto', fontSize: '13px' }}>
                        <div style={{ fontWeight: 'bold', marginBottom: '8px', color: '#ccc' }}>Mesa {comandaParaEnviar.numero_mesa}</div>
                        {cart[comandaParaEnviar.comandaId].map((it, idx) => (
                            <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #333', padding: '4px 0' }}>
                                <span style={{ color: '#aaa' }}>{it.quantidade}x {it.nome}</span>
                                <span style={{ color: '#fff' }}>R$ {(it.preco * it.quantidade).toFixed(2)}</span>
                            </div>
                        ))}
                        <div style={{ textAlign: 'right', marginTop: '8px', fontWeight: 'bold', color: 'var(--primary-red)' }}>
                            Total Parcial: R$ {calcularTotalLocal(comandaParaEnviar.comandaId).toFixed(2)}
                        </div>
                    </div>
                )}
            </ConfirmDialog>

            <ConfirmDialog 
                isOpen={!!contaParaFechar}
                title="Fechar conta da mesa?"
                description="Confirme se o pagamento já foi efetuado pelo cliente. Após fechar a conta, a comanda será finalizada."
                confirmLabel="Fechar conta e liberar comanda"
                cancelLabel="Cancelar"
                variant="success"
                isLoading={isProcessing}
                onConfirm={confirmarFechamentoConta}
                onCancel={() => setContaParaFechar(null)}
            />

            <ConfirmDialog 
                isOpen={!!comandaParaCancelar}
                title="Cancelar esta comanda?"
                description={`A comanda #${comandaParaCancelar} da Mesa ${expandedMesa} será cancelada permanentemente. Esta ação não pode ser desfeita.`}
                confirmLabel="Cancelar comanda"
                cancelLabel="Manter comanda"
                variant="danger"
                isLoading={isProcessing}
                onConfirm={confirmarCancelamentoComanda}
                onCancel={() => setComandaParaCancelar(null)}
            />

        </SalaoLayout>
    );
}