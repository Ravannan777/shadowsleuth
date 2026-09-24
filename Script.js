// Real-time Clock Updater in Header Bar
setInterval(() => {
    const now = new Date();
    const timeString = now.toTimeString().split(' ')[0];
    const clockEl = document.getElementById('clock');
    if (clockEl) {
        clockEl.innerText = timeString;
    }
}, 1000);

// Simulated Live C2 Server Heartbeat & Telemetry Logs
setInterval(() => {
    const logsContainer = document.getElementById('terminalLogs');
    if (logsContainer) {
        const timeTag = new Date().toTimeString().split(' ')[0];
        const p = document.createElement('p');
        p.style.color = '#4ade80';
        p.innerHTML = `[${timeTag}] <span>[SECURE HEARTBEAT]</span> C2 node connection active... Calicut gateway stable.`;
        logsContainer.appendChild(p);
        logsContainer.scrollTop = logsContainer.scrollHeight;
    }
}, 6000);