import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function ConfirmDialog({
    isOpen,
    title,
    description,
    confirmLabel = 'Confirmar',
    cancelLabel = 'Cancelar',
    variant = 'primary', // 'danger', 'warning', 'primary', 'success'
    isLoading = false,
    onConfirm,
    onCancel,
    children
}) {
    // Fechar ao pressionar ESC
    useEffect(() => {
        const handleKeyDown = (e) => {
            if (e.key === 'Escape' && isOpen && !isLoading) {
                onCancel();
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [isOpen, isLoading, onCancel]);

    if (!isOpen) return null;

    // Estilos baseados na variante
    const variantStyles = {
        primary: { background: 'linear-gradient(90deg, var(--primary-red), #e60000)', color: '#fff' }, // O tema do app é focado em vermelho
        danger: { background: 'linear-gradient(90deg, #aa0000, #ff3333)', color: '#fff' },
        warning: { background: 'linear-gradient(90deg, #cc7700, #ffaa00)', color: '#111' },
        success: { background: 'linear-gradient(90deg, #004a00, #008b00)', color: '#fff' },
    };

    const confirmStyle = variantStyles[variant] || variantStyles.primary;

    return (
        <AnimatePresence>
            <div 
                style={{ 
                    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, 
                    background: 'rgba(0,0,0,0.85)', zIndex: 9999, 
                    display: 'flex', justifyContent: 'center', alignItems: 'center',
                    backdropFilter: 'blur(4px)'
                }}
            >
                <motion.div 
                    initial={{ opacity: 0, scale: 0.95, y: 10 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.95, y: 10 }}
                    className="card" 
                    style={{ 
                        width: '90%', maxWidth: '420px', 
                        background: '#1a1a1a', border: '1px solid #333', 
                        boxShadow: '0 10px 40px rgba(0,0,0,0.5)',
                        padding: '24px'
                    }}
                >
                    <h2 style={{ color: '#fff', fontSize: '18px', marginBottom: '10px' }}>{title}</h2>
                    
                    {description && (
                        <p style={{ color: '#aaa', fontSize: '14px', marginBottom: '20px', lineHeight: '1.4' }}>
                            {description}
                        </p>
                    )}

                    {children && (
                        <div style={{ marginBottom: '20px', background: '#111', padding: '12px', borderRadius: '6px', border: '1px solid #222' }}>
                            {children}
                        </div>
                    )}

                    <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '10px' }}>
                        <button 
                            onClick={onCancel} 
                            disabled={isLoading}
                            style={{ 
                                background: 'transparent', color: '#ccc', border: '1px solid #444',
                                opacity: isLoading ? 0.5 : 1, cursor: isLoading ? 'not-allowed' : 'pointer',
                                padding: '10px 16px'
                            }}
                        >
                            {cancelLabel}
                        </button>
                        <motion.button 
                            whileHover={!isLoading ? { scale: 1.02 } : {}} 
                            whileTap={!isLoading ? { scale: 0.98 } : {}}
                            onClick={onConfirm} 
                            disabled={isLoading}
                            style={{ 
                                ...confirmStyle, 
                                border: 'none', fontWeight: 'bold',
                                opacity: isLoading ? 0.7 : 1, cursor: isLoading ? 'wait' : 'pointer',
                                padding: '10px 20px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px'
                            }}
                        >
                            {isLoading && <span className="spinner" style={{ width: '14px', height: '14px', border: '2px solid currentColor', borderRightColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></span>}
                            {isLoading ? 'Aguarde...' : confirmLabel}
                        </motion.button>
                    </div>
                </motion.div>
                <style>{`
                    @keyframes spin { 100% { transform: rotate(360deg); } }
                `}</style>
            </div>
        </AnimatePresence>
    );
}
