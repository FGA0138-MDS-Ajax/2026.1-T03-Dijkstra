import React from 'react';
import '../assets/css/kitchen-timer.css';

export default function KitchenTimeBadge({ status }) {
    let text = "";
    let badgeClass = "";

    switch (status) {
        case 'on_time':
            text = "No Prazo";
            badgeClass = "kitchen-badge--on-time";
            break;
        case 'warning':
            text = "Atenção";
            badgeClass = "kitchen-badge--warning";
            break;
        case 'late':
            text = "Atrasado";
            badgeClass = "kitchen-badge--late";
            break;
        case 'ready':
            text = "Pronto";
            badgeClass = "kitchen-badge--ready";
            break;
        case 'waiting':
            text = "Aguardando";
            badgeClass = "kitchen-badge--ready"; // Use plain style for waiting
            break;
        default:
            return null;
    }

    return (
        <span className={`kitchen-badge ${badgeClass}`}>
            {text}
        </span>
    );
}
