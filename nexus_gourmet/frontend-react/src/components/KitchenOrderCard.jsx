import React, { useState, useCallback } from 'react';
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

    return (
        <div className={`kitchen-order-card ${cardClass}`}>
            <div className="kitchen-order-card__header">
                <h3 className="kitchen-order-card__title">
                    Mesa {order.mesa?.numero} <span style={{ fontSize: '12px', color: '#888' }}>#{order.id}</span>
                </h3>
                <KitchenTimeBadge status={isReady ? 'ready' : (order.sent_to_kitchen_at ? statusColor : 'waiting')} />
            </div>

            <div className="kitchen-order-card__meta">
                <span>
                    ⏱️ <KitchenOrderTimer 
                        sentToKitchenAt={order.sent_to_kitchen_at} 
                        estimatedMinutes={order.estimated_preparation_minutes || 15}
                        isReady={isReady}
                        onStatusChange={handleStatusChange}
                    /> 
                    <span style={{ fontSize: '10px', marginLeft: '4px' }}>
                        / {order.estimated_preparation_minutes || 15}m
                    </span>
                </span>
                <span style={{ background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: '4px' }}>
                    {order.status}
                </span>
            </div>

            <ul className="kitchen-order-card__items">
                {order.itens.map(item => (
                    <li key={item.id}>
                        {item.quantidade}x - {item.produto || 'Item apagado'}
                        {item.observacao && <span className="kitchen-order-card__obs">Obs: {item.observacao}</span>}
                    </li>
                ))}
            </ul>

            {!isReady && (
                <button 
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
                </button>
            )}
        </div>
    );
}
