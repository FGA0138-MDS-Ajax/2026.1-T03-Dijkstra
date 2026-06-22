import React, { useState, useEffect } from 'react';
import '../assets/css/kitchen-timer.css';

export default function KitchenOrderTimer({ sentToKitchenAt, estimatedMinutes, isReady, onStatusChange }) {
    const [elapsedSeconds, setElapsedSeconds] = useState(0);

    useEffect(() => {
        if (!sentToKitchenAt || isReady) {
            return;
        }

        const sentTime = new Date(sentToKitchenAt + 'Z'); // Assume UTC from backend

        const updateTimer = () => {
            const now = new Date();
            const diffSecs = Math.floor((now - sentTime) / 1000);
            setElapsedSeconds(diffSecs > 0 ? diffSecs : 0);
        };

        updateTimer();
        const intervalId = setInterval(updateTimer, 1000);

        return () => clearInterval(intervalId);
    }, [sentToKitchenAt, isReady]);

    useEffect(() => {
        if (isReady) {
            onStatusChange('ready');
            return;
        }
        if (!sentToKitchenAt) {
            onStatusChange('waiting');
            return;
        }

        const estimatedSecs = estimatedMinutes * 60;
        let newStatus = 'on_time';

        if (estimatedSecs > 0) {
            const percent = elapsedSeconds / estimatedSecs;
            if (percent > 1.0) {
                newStatus = 'late';
            } else if (percent >= 0.7) {
                newStatus = 'warning';
            }
        }

        onStatusChange(newStatus);
    }, [elapsedSeconds, estimatedMinutes, isReady, sentToKitchenAt, onStatusChange]);

    if (!sentToKitchenAt) {
        return <span className="kitchen-timer-text kitchen-timer-text--ready">--:--</span>;
    }

    const minutes = Math.floor(elapsedSeconds / 60);
    const seconds = elapsedSeconds % 60;
    const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    let textColorClass = 'kitchen-timer-text--on-time';
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
