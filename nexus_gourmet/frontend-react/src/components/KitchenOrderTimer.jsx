import React, { useState, useEffect } from 'react';
import '../assets/css/kitchen-timer.css';

export default function KitchenOrderTimer({ tempoDecorridoStr, estimatedMinutes, isReady, onStatusChange }) {
    const [localSeconds, setLocalSeconds] = useState(0);

    // 1. Sincroniza o tempo sempre que a API trouxer dados novos (a cada 15s)
    useEffect(() => {
        if (!tempoDecorridoStr || tempoDecorridoStr === 'Não iniciado') {
            setLocalSeconds(0);
            return;
        }
        let mins = 0;
        let secs = 0;
        const mMatch = tempoDecorridoStr.match(/(\d+)m/);
        const sMatch = tempoDecorridoStr.match(/(\d+)s/);
        
        if (mMatch) mins = parseInt(mMatch[1], 10);
        if (sMatch) secs = parseInt(sMatch[1], 10);
        
        setLocalSeconds((mins * 60) + secs);
    }, [tempoDecorridoStr]);

    // 2. Roda o timer em tempo real (1 em 1 segundo) no front-end
    useEffect(() => {
        if (isReady || !tempoDecorridoStr || tempoDecorridoStr === 'Não iniciado') return;

        const interval = setInterval(() => {
            setLocalSeconds(prev => prev + 1);
        }, 1000);

        return () => clearInterval(interval);
    }, [isReady, tempoDecorridoStr]);

    // 3. Atualiza os status de atraso com base no tempo local
    useEffect(() => {
        if (isReady) {
            onStatusChange('ready');
            return;
        }
        if (!tempoDecorridoStr || tempoDecorridoStr === 'Não iniciado') {
            onStatusChange('waiting');
            return;
        }

        const estimatedSecs = estimatedMinutes * 60;
        let newStatus = 'on_time';
        if (estimatedSecs > 0) {
            const percent = localSeconds / estimatedSecs;
            if (percent > 1.0) newStatus = 'late';
            else if (percent >= 0.7) newStatus = 'warning';
        }
        onStatusChange(newStatus);
    }, [localSeconds, estimatedMinutes, isReady, tempoDecorridoStr, onStatusChange]);

    if (!tempoDecorridoStr || tempoDecorridoStr === 'Não iniciado') {
        return <span className="kitchen-timer-text kitchen-timer-text--ready">--:--</span>;
    }

    // Calcula de volta para exibição MM:SS
    const displayMins = Math.floor(localSeconds / 60);
    const displaySecs = localSeconds % 60;
    const formattedTime = `${String(displayMins).padStart(2, '0')}:${String(displaySecs).padStart(2, '0')}`;

    let textColorClass = 'kitchen-timer-text--on-time';
    const estimatedSecs = estimatedMinutes * 60;

    if (isReady) {
        textColorClass = 'kitchen-timer-text--ready';
    } else if (estimatedSecs > 0) {
        const percent = localSeconds / estimatedSecs;
        if (percent > 1.0) textColorClass = 'kitchen-timer-text--late';
        else if (percent >= 0.7) textColorClass = 'kitchen-timer-text--warning';
    }

    return (
        <span className={`kitchen-timer-text ${textColorClass}`}>
            {formattedTime}
        </span>
    );
}