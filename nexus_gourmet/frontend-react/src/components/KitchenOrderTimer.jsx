import React, { useEffect } from 'react';
import '../assets/css/kitchen-timer.css';

export default function KitchenOrderTimer({ tempoDecorridoStr, estimatedMinutes, isReady, onStatusChange }) {
    
    // CORREÇÃO GERAL: Utilizando a string de tempo_decorrido que vem pronta do Backend "Xm Ys"

    useEffect(() => {
        if (isReady) {
            onStatusChange('ready');
            return;
        }
        if (!tempoDecorridoStr || tempoDecorridoStr === 'Não iniciado') {
            onStatusChange('waiting');
            return;
        }

        let mins = 0;
        let secs = 0;
        const mMatch = tempoDecorridoStr.match(/(\d+)m/);
        const sMatch = tempoDecorridoStr.match(/(\d+)s/);
        if (mMatch) mins = parseInt(mMatch[1], 10);
        if (sMatch) secs = parseInt(sMatch[1], 10);

        const elapsedSeconds = (mins * 60) + secs;
        const estimatedSecs = estimatedMinutes * 60;
        let newStatus = 'on_time';

        if (estimatedSecs > 0) {
            const percent = elapsedSeconds / estimatedSecs;
            if (percent > 1.0) newStatus = 'late';
            else if (percent >= 0.7) newStatus = 'warning';
        }

        onStatusChange(newStatus);
    }, [tempoDecorridoStr, estimatedMinutes, isReady, onStatusChange]);

    if (!tempoDecorridoStr || tempoDecorridoStr === 'Não iniciado') {
        return <span className="kitchen-timer-text kitchen-timer-text--ready">--:--</span>;
    }

    let mins = 0;
    let secs = 0;
    const mMatch = tempoDecorridoStr.match(/(\d+)m/);
    const sMatch = tempoDecorridoStr.match(/(\d+)s/);
    if (mMatch) mins = parseInt(mMatch[1], 10);
    if (sMatch) secs = parseInt(sMatch[1], 10);

    const formattedTime = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

    let textColorClass = 'kitchen-timer-text--on-time';
    const elapsedSeconds = (mins * 60) + secs;
    const estimatedSecs = estimatedMinutes * 60;
    
    if (isReady) {
        textColorClass = 'kitchen-timer-text--ready';
    } else if (estimatedSecs > 0) {
        const percent = elapsedSeconds / estimatedSecs;
        if (percent > 1.0) textColorClass = 'kitchen-timer-text--late';
        else if (percent >= 0.7) textColorClass = 'kitchen-timer-text--warning';
    }

    return (
        <span className={`kitchen-timer-text ${textColorClass}`}>
            {formattedTime}
        </span>
    );
}