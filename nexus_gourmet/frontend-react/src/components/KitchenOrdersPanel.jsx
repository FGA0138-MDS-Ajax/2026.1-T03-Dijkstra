import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { AnimatePresence } from 'framer-motion';
import KitchenOrderCard from './KitchenOrderCard';
import '../assets/css/kitchen-timer.css';

export default function KitchenOrdersPanel({ onConcluirPedido }) {
    const [pedidos, setPedidos] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    const fetchPedidos = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/cozinha/fila', { withCredentials: true });
            if (response.data.success) {
                // Filtra pedidos relevantes para a cozinha
                const emPreparo = response.data.data.filter(p => p.status === 'Em Preparo');
                setPedidos(emPreparo);
            }
        } catch (err) {
            console.error('Erro ao buscar pedidos da cozinha', err);
            toast.error('Erro de conexão ao buscar fila de preparo.');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchPedidos();
        const interval = setInterval(fetchPedidos, 15000); // Polling a cada 15 segundos
        return () => clearInterval(interval);
    }, []);

    const handleConcluir = async (numero_mesa, comanda_id) => {
        if (onConcluirPedido) {
            try {
                await onConcluirPedido(numero_mesa, comanda_id);
                toast.success('🍽️ Pedido marcado como Pronto!');
                fetchPedidos();
            } catch (err) {
                toast.error('❌ Não foi possível concluir a ação.');
            }
        }
    };

    return (
        <div className="kitchen-orders-panel-container">
            <div className="kitchen-orders-panel">
                {isLoading ? (
                    Array.from({ length: 4 }).map((_, idx) => (
                        <div key={`skeleton-${idx}`} className="kitchen-order-card skeleton" style={{ height: '200px' }}>
                            <div className="skeleton-text" style={{ width: '40%', marginBottom: '10px' }}></div>
                            <div className="skeleton-text" style={{ width: '80%', marginBottom: '20px' }}></div>
                            <div className="skeleton-text" style={{ width: '60%', marginBottom: '10px' }}></div>
                            <div className="skeleton-text" style={{ width: '60%', marginBottom: 'auto' }}></div>
                            <div className="skeleton-btn" style={{ width: '100%', marginTop: '10px' }}></div>
                        </div>
                    ))
                ) : (
                    <AnimatePresence>
                        {pedidos.map(pedido => (
                            <KitchenOrderCard 
                                key={pedido.id} 
                                order={pedido} 
                                onConcluir={handleConcluir} 
                            />
                        ))}
                    </AnimatePresence>
                )}
                {!isLoading && pedidos.length === 0 && (
                    <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', gridColumn: '1 / -1' }}>
                        Nenhum pedido pendente no momento.
                    </p>
                )}
            </div>
        </div>
    );
}
