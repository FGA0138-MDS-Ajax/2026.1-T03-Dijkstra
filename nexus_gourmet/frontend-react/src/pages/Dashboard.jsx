import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { motion } from 'framer-motion';
import AdminLayout from '../components/AdminLayout';
import ConfirmDialog from '../components/ConfirmDialog';

export default function Dashboard() {
    const [stats, setStats] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isRefreshing, setIsRefreshing] = useState(false);
    
    // Estados do novo modal de fechamento
    const [modalEncerrar, setModalEncerrar] = useState(false);
    const [isClosing, setIsClosing] = useState(false);

    const fetchStats = async (isManual = false) => {
        if (isManual) setIsRefreshing(true);
        try {
            const response = await axios.get('http://localhost:5000/api/usuarios/finalizar_dia', { withCredentials: true });
            if (response.data.success) {
                setStats(response.data.data);
                if (isManual) toast.success('📊 Relatório atualizado!');
            }
        } catch (err) {
            toast.error('Erro ao carregar estatísticas do dia.');
        } finally {
            setIsLoading(false);
            setIsRefreshing(false);
        }
    };

    useEffect(() => { fetchStats(); }, []);

    // Função que aciona a nova rota POST que criamos no Python
    const encerrarExpediente = async () => {
    setIsClosing(true);
    try {
        // Exemplo de chamada para a rota (você precisará criar esta lógica no backend)
        await axios.post('http://localhost:5000/api/usuarios/encerrar_caixa', {}, { withCredentials: true });
        
        toast.success('✨ Caixa fechado com sucesso!');
        setModalEncerrar(false);
        fetchStats(true); // Recarrega os dados via API em vez de dar reload na tela
    } catch (err) {
        toast.error('Erro ao fechar o caixa.');
    } finally {
        setIsClosing(false);
    }
};

    const cards = [
        { icon: '📋', label: 'Comandas do Dia', value: stats?.total_comandas ?? 0, gradient: 'linear-gradient(135deg, #1a0000, #3a0000)', border: '#cc0000' },
        { icon: '💰', label: 'Faturamento Total', value: `R$ ${(stats?.total_faturamento ?? 0).toFixed(2)}`, gradient: 'linear-gradient(135deg, #001a00, #003a00)', border: '#00cc66' },
        { icon: '🍽️', label: 'Itens Vendidos', value: stats?.total_itens ?? 0, gradient: 'linear-gradient(135deg, #0a0a1a, #1a1a3a)', border: '#6666ff' },
        { icon: '❌', label: 'Comandas Canceladas', value: stats?.total_comandas_canceladas ?? 0, gradient: 'linear-gradient(135deg, #1a1a00, #3a3a00)', border: '#ffaa00' },
    ];

    return (
        <AdminLayout>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '20px' }}>
                <h2 className="page-title" style={{ marginBottom: 0 }}>Dashboard — Estatísticas</h2>
                
                <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                    <motion.button 
                        whileHover={{ scale: 1.05 }} 
                        whileTap={{ scale: 0.95 }}
                        onClick={() => fetchStats(true)}
                        disabled={isRefreshing}
                        style={{ background: '#333', padding: '10px 15px', opacity: isRefreshing ? 0.7 : 1 }}
                    >
                        {isRefreshing ? 'Atualizando...' : '🔄 Atualizar'}
                    </motion.button>

                    <motion.button 
                        whileHover={{ scale: 1.05 }} 
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setModalEncerrar(true)}
                        style={{ background: 'linear-gradient(90deg, #cc0000, #ff3333)', padding: '10px 15px', fontWeight: 'bold' }}
                    >
                        🔒 Fechar Caixa Diário
                    </motion.button>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '20px', marginTop: '8px' }}>
                {cards.map((card, idx) => (
                    <motion.div 
                        key={card.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: idx * 0.1 }}
                        style={{ background: card.gradient, border: `1px solid ${card.border}`, borderRadius: '14px', padding: '28px 24px', display: 'flex', flexDirection: 'column', gap: '12px', boxShadow: `0 4px 20px ${card.border}22` }}
                    >
                        <div style={{ fontSize: 'clamp(24px, 6vw, 32px)' }}>{card.icon}</div>
                        <div style={{ fontSize: '11px', fontWeight: 700, letterSpacing: '2px', textTransform: 'uppercase', color: '#888' }}>{card.label}</div>
                        {isLoading ? (
                            <div className="skeleton skeleton-text" style={{ width: '80px', height: '36px' }}></div>
                        ) : (
                            <div style={{ fontSize: 'clamp(22px, 7vw, 32px)', fontWeight: 900, color: '#fff', fontFamily: "'Rubik', sans-serif", letterSpacing: '-1px' }}>{card.value}</div>
                        )}
                    </motion.div>
                ))}
            </div>

            <ConfirmDialog 
                isOpen={modalEncerrar}
                title="Encerrar Expediente?"
                description="O sistema irá varrer todas as comandas. Esta ação irá falhar se existirem clientes ainda consumindo no salão."
                confirmLabel="Finalizar Dia"
                cancelLabel="Cancelar"
                variant="danger"
                isLoading={isClosing}
                onConfirm={encerrarExpediente}
                onCancel={() => setModalEncerrar(false)}
            />
        </AdminLayout>
    );
}