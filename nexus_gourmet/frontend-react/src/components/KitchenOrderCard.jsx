import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import KitchenOrderTimer from './KitchenOrderTimer';
import KitchenTimeBadge from './KitchenTimeBadge';
import '../assets/css/kitchen-timer.css';

export default function KitchenOrderCard({ order, onConcluir }) {
    const [statusColor, setStatusColor] = useState('on_time');

    const handleStatusChange = useCallback((newStatus) => {
        setStatusColor(newStatus);
    }, []);

    const isReady = order.status === 'Pronto' || order.status === 'Entregue' || order.status === 'Cancelado';
    
    let cardClass = '';
    if (isReady) {
        cardClass = 'kitchen-order-card--ready';
    } else if (statusColor === 'late') {
        cardClass = 'kitchen-order-card--late';
    } else if (statusColor === 'warning') {
        cardClass = 'kitchen-order-card--warning';
    } else {
        cardClass = 'kitchen-order-card--on-time';
    }

    // CORREÇÃO: Filtramos para exibir apenas os itens que estão ativos na cozinha agora.
    // Ignoramos itens já entregues (PRONTO) ou recém colocados na comanda e não enviados (PENDENTE)
    const itensAtivos = order.itens?.filter(item => item.cozinha_status === 'PREPARANDO') || [];

    // Calcula o tempo estimado focado apenas nos itens que a cozinha tem que preparar no momento
    const estMinutes = itensAtivos.length 
        ? Math.max(...itensAtivos.map(i => i.preparation_time_minutes || 15)) 
        : 15;

    // Prevenção visual: se a comanda constar no salão como "Em Preparo", mas a cozinha já clicou 
    // e os itens ainda estão processando a saída da tela, ele não renderiza um card vazio.
    if (!isReady && itensAtivos.length === 0) {
        return null;
    }

    return (
        <motion.div 
            layout
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95, transition: { duration: 0.2 } }}
            transition={{ duration: 0.3 }}
            className={`kitchen-order-card ${cardClass}`}
        >
            <div className="kitchen-order-card__header">
                <h3 className="kitchen-order-card__title">
                    Mesa {order.mesa?.numero} <span style={{ fontSize: '12px', color: '#888' }}>#{order.id}</span>
                </h3>
                <KitchenTimeBadge status={isReady ? 'ready' : (order.tempo_decorrido && order.tempo_decorrido !== 'Não iniciado' ? statusColor : 'waiting')} />
            </div>

            <div className="kitchen-order-card__meta">
                <span>
                    ⏱️ <KitchenOrderTimer 
                        tempoDecorridoStr={order.tempo_decorrido} 
                        estimatedMinutes={estMinutes}
                        isReady={isReady}
                        onStatusChange={handleStatusChange}
                    /> 
                    <span style={{ fontSize: '10px', marginLeft: '4px' }}>
                        / {estMinutes}m
                    </span>
                </span>
                <span style={{ background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: '4px' }}>
                    {order.status}
                </span>
            </div>

            <ul className="kitchen-order-card__items">
                {/* CORREÇÃO: Mapeamos o array de itens ativos ao invés de todo o histórico */}
                {itensAtivos.map(item => (
                    <li key={item.id}>
                        {item.quantidade}x - {item.produto || 'Item apagado'}
                        {item.observacao && <span className="kitchen-order-card__obs">Obs: {item.observacao}</span>}
                    </li>
                ))}
            </ul>

            {!isReady && (
                <motion.button 
                    whileHover={{ scale: 1.02 }} 
                    whileTap={{ scale: 0.98 }}
                    onClick={() => onConcluir(order.mesa?.numero, order.id)} 
                    style={{ 
                        width: '100%', 
                        background: 'linear-gradient(90deg, #004a00, #008b00)',
                        padding: '10px 5px',
                        textAlign: 'center',
                        marginTop: 'auto',
                        border: 'none',
                        color: 'white',
                        fontWeight: 'bold',
                        cursor: 'pointer',
                        borderRadius: '4px'
                    }}
                >
                    Marcar como Pronto
                </motion.button>
            )}
        </motion.div>
    );
}