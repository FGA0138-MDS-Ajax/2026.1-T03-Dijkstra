import React, { useState, useEffect } from 'react';
import axios from 'axios';
import KitchenOrderCard from './KitchenOrderCard';
import '../assets/css/kitchen-timer.css';

export default function KitchenOrdersPanel({ onConcluirPedido }) {
    const [pedidos, setPedidos] = useState([]);
    const [error, setError] = useState(null);

    const fetchPedidos = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/cozinha/fila', { withCredentials: true });
            if (response.data.success) {
                // Filtra pedidos relevantes para a cozinha
                const emPreparo = response.data.data.filter(p => p.status === 'Em Preparo');
                setPedidos(emPreparo);
                setError(null);
            }
        } catch (err) {
            console.error('Erro ao buscar pedidos da cozinha', err);
            setError('Erro de conexão ao buscar fila de preparo.');
        }
    };

    useEffect(() => {
        fetchPedidos();
        const interval = setInterval(fetchPedidos, 15000); // Polling a cada 15 segundos
        return () => clearInterval(interval);
    }, []);

    const handleConcluir = async (numero_mesa, comanda_id) => {
        if (onConcluirPedido) {
            await onConcluirPedido(numero_mesa, comanda_id);
            fetchPedidos();
        }
    };

    return (
        <div className="kitchen-orders-panel-container">
            {error && <div style={{ color: '#ff5555', marginBottom: '10px' }}>{error}</div>}
            <div className="kitchen-orders-panel">
                {pedidos.map(pedido => (
                    <KitchenOrderCard 
                        key={pedido.id} 
                        order={pedido} 
                        onConcluir={handleConcluir} 
                    />
                ))}
                {pedidos.length === 0 && (
                    <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', gridColumn: '1 / -1' }}>
                        Nenhum pedido pendente no momento.
                    </p>
                )}
            </div>
        </div>
    );
}
