import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { AnimatePresence } from 'framer-motion';
import KitchenOrderCard from './KitchenOrderCard';
import ConfirmDialog from './ConfirmDialog';
import '../assets/css/kitchen-timer.css';

export default function KitchenOrdersPanel({ onConcluirPedido }) {
    const [pedidos, setPedidos] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    const [pedidoParaConcluir, setPedidoParaConcluir] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);

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

    const prepararConclusao = (numero_mesa, comanda_id) => {
        setPedidoParaConcluir({ numero_mesa, comanda_id });
    };

    const confirmarConclusao = async () => {
        if (!pedidoParaConcluir || !onConcluirPedido) return;
        setIsProcessing(true);
        try {
            await onConcluirPedido(pedidoParaConcluir.numero_mesa, pedidoParaConcluir.comanda_id);
            toast.success('🍽️ Pedido marcado como Pronto!');
            fetchPedidos();
            setPedidoParaConcluir(null);
        } catch (err) {
            toast.error('❌ Não foi possível concluir a ação.');
        } finally {
            setIsProcessing(false);
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
                                    onConcluir={prepararConclusao} 
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

            <ConfirmDialog 
                isOpen={!!pedidoParaConcluir}
                title="Marcar pedido como pronto?"
                description={`Mesa ${pedidoParaConcluir?.numero_mesa} - Comanda #${pedidoParaConcluir?.comanda_id}. Confirme se todos os itens foram preparados corretamente.`}
                confirmLabel="Marcar como pronto"
                cancelLabel="Cancelar"
                variant="success"
                isLoading={isProcessing}
                onConfirm={confirmarConclusao}
                onCancel={() => setPedidoParaConcluir(null)}
            />

        </div>
    );
}
