import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { motion } from 'framer-motion';
import AdminLayout from '../components/AdminLayout';

export default function Dashboard() {
    const [stats, setStats] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const fetchStats = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/admin/estatisticas', { withCredentials: true });
            if (response.data.success) {
                setStats(response.data.data);
            }
        } catch (err) {
            console.error(err);
            toast.error('Erro ao carregar estatísticas.');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => { fetchStats(); }, []);

    const cards = [
        { 
            icon: '📋', 
            label: 'Comandas do Dia', 
            value: stats?.total_comandas ?? 0, 
            gradient: 'linear-gradient(135deg, #1a0000, #3a0000)',
            border: '#cc0000'
        },
        { 
            icon: '💰', 
            label: 'Faturamento Total', 
            value: `R$ ${(stats?.total_faturamento ?? 0).toFixed(2)}`, 
            gradient: 'linear-gradient(135deg, #001a00, #003a00)',
            border: '#00cc66'
        },
        { 
            icon: '🍽️', 
            label: 'Itens Vendidos', 
            value: stats?.total_itens ?? 0, 
            gradient: 'linear-gradient(135deg, #0a0a1a, #1a1a3a)',
            border: '#6666ff'
        },
        { 
            icon: '❌', 
            label: 'Comandas Canceladas', 
            value: stats?.total_comandas_canceladas ?? 0, 
            gradient: 'linear-gradient(135deg, #1a1a00, #3a3a00)',
            border: '#ffaa00'
        },
    ];

    return (
        <AdminLayout>
            <h2 className="page-title">Dashboard — Estatísticas do Dia</h2>

            <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', 
                gap: '20px',
                marginTop: '8px'
            }}>
                {cards.map((card, idx) => (
                    <motion.div 
                        key={card.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: idx * 0.1 }}
                        style={{
                            background: card.gradient,
                            border: `1px solid ${card.border}`,
                            borderRadius: '14px',
                            padding: '28px 24px',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '12px',
                            boxShadow: `0 4px 20px ${card.border}22`,
                            transition: 'transform 0.2s, box-shadow 0.2s',
                        }}
                        whileHover={{ scale: 1.03, boxShadow: `0 8px 30px ${card.border}33` }}
                    >
                        <div style={{ fontSize: '32px' }}>{card.icon}</div>
                        <div style={{ 
                            fontSize: '11px', 
                            fontWeight: 700, 
                            letterSpacing: '2px', 
                            textTransform: 'uppercase', 
                            color: '#888' 
                        }}>
                            {card.label}
                        </div>
                        {isLoading ? (
                            <div className="skeleton skeleton-text" style={{ width: '80px', height: '36px' }}></div>
                        ) : (
                            <div style={{ 
                                fontSize: '32px', 
                                fontWeight: 900, 
                                color: '#fff',
                                fontFamily: "'Rubik', sans-serif",
                                letterSpacing: '-1px'
                            }}>
                                {card.value}
                            </div>
                        )}
                    </motion.div>
                ))}
            </div>

            <div className="card" style={{ marginTop: '24px', textAlign: 'center', padding: '20px' }}>
                <p style={{ color: '#555', fontSize: '13px' }}>
                    📊 As estatísticas são atualizadas a cada carregamento da página. Dados referentes ao dia atual.
                </p>
            </div>
        </AdminLayout>
    );
}
