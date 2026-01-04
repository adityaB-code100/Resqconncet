/**
 * Alerts Web Component
 * Modern alternative to iframes using Web Components
 */

class AlertsWidget extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.data = null;
        this.updateInterval = null;
    }

    connectedCallback() {
        this.render();
        this.loadData();
        this.startAutoUpdate();
    }

    disconnectedCallback() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    font-family: 'Plus Jakarta Sans', Arial, sans-serif;
                }
                
                .alerts-container {
                    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%);
                    backdrop-filter: blur(20px);
                    border: 1px solid rgba(255,255,255,0.3);
                    border-radius: 16px;
                    padding: 16px;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                    max-height: 400px;
                    overflow-y: auto;
                }
                
                .header {
                    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 50%, #a93226 100%);
                    color: white;
                    padding: 12px;
                    border-radius: 12px;
                    margin-bottom: 16px;
                    position: relative;
                    overflow: hidden;
                }
                
                .header::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    right: 0;
                    width: 80px;
                    height: 80px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 50%;
                    transform: translate(40px, -40px);
                }
                
                .header-content {
                    position: relative;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }
                
                .title {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                
                .title-icon {
                    width: 32px;
                    height: 32px;
                    background: rgba(255,255,255,0.2);
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    backdrop-filter: blur(10px);
                    animation: float 6s ease-in-out infinite;
                }
                
                @keyframes float {
                    0%, 100% { transform: translateY(0px); }
                    50% { transform: translateY(-5px); }
                }
                
                .title-text h3 {
                    margin: 0;
                    font-size: 16px;
                    font-weight: bold;
                }
                
                .title-text p {
                    margin: 0;
                    font-size: 12px;
                    opacity: 0.8;
                }
                
                .status {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-size: 12px;
                }
                
                .status-dot {
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    animation: pulse 2s infinite;
                }
                
                .status-dot.active {
                    background: #f39c12;
                }
                
                .status-dot.clear {
                    background: #00b894;
                }
                
                .status-dot.offline {
                    background: #e17055;
                }
                
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
                
                .alerts-list {
                    display: flex;
                    flex-direction: column;
                    gap: 12px;
                }
                
                .alert-item {
                    background: rgba(255, 248, 248, 0.95);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(231, 76, 60, 0.2);
                    border-left: 4px solid #e74c3c;
                    border-radius: 12px;
                    overflow: hidden;
                    transition: all 0.3s ease;
                    opacity: 0;
                    transform: translateY(20px);
                    animation: slideIn 0.5s ease forwards;
                }
                
                .alert-item:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 24px rgba(231, 76, 60, 0.2);
                }
                
                @keyframes slideIn {
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                .alert-header {
                    background: linear-gradient(135deg, #e74c3c, #f39c12);
                    color: white;
                    padding: 8px 12px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                
                .alert-icon {
                    width: 20px;
                    height: 20px;
                    background: rgba(255,255,255,0.2);
                    border-radius: 6px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 10px;
                }
                
                .alert-title {
                    flex: 1;
                    font-size: 12px;
                    font-weight: bold;
                    line-height: 1.2;
                }
                
                .alert-pulse {
                    width: 6px;
                    height: 6px;
                    background: #f1c40f;
                    border-radius: 50%;
                    animation: pulse 2s infinite;
                }
                
                .alert-content {
                    padding: 8px 12px;
                    display: flex;
                    flex-direction: column;
                    gap: 6px;
                }
                
                .alert-detail {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-size: 11px;
                }
                
                .detail-icon {
                    width: 16px;
                    height: 16px;
                    border-radius: 4px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 8px;
                }
                
                .category-icon { background: rgba(52, 152, 219, 0.2); color: #3498db; }
                .date-icon { background: rgba(46, 204, 113, 0.2); color: #2ecc71; }
                .location-icon { background: rgba(155, 89, 182, 0.2); color: #9b59b6; }
                
                .detail-label {
                    color: #666;
                    font-weight: 500;
                }
                
                .detail-value {
                    font-weight: 600;
                }
                
                .category-value { color: #3498db; }
                .date-value { color: #2ecc71; }
                .location-value { color: #9b59b6; }
                
                .no-alerts {
                    text-align: center;
                    padding: 32px 16px;
                    color: #666;
                }
                
                .no-alerts-icon {
                    width: 48px;
                    height: 48px;
                    background: rgba(46, 204, 113, 0.2);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 12px;
                    font-size: 20px;
                    color: #2ecc71;
                }
                
                .loading {
                    text-align: center;
                    padding: 32px;
                    color: #666;
                }
                
                .loading-spinner {
                    width: 32px;
                    height: 32px;
                    border: 3px solid #f3f3f3;
                    border-top: 3px solid #e74c3c;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 12px;
                }
                
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                
                .error {
                    text-align: center;
                    padding: 32px;
                    color: #e17055;
                }
                
                .retry-btn {
                    background: #e74c3c;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 12px;
                    margin-top: 8px;
                }
                
                .retry-btn:hover {
                    background: #c0392b;
                }
                
                .footer {
                    margin-top: 16px;
                    padding-top: 12px;
                    border-top: 1px solid rgba(0,0,0,0.1);
                    text-align: center;
                    font-size: 11px;
                    color: #666;
                }
                
                /* Custom scrollbar */
                .alerts-container::-webkit-scrollbar {
                    width: 6px;
                }
                
                .alerts-container::-webkit-scrollbar-track {
                    background: rgba(0,0,0,0.1);
                    border-radius: 3px;
                }
                
                .alerts-container::-webkit-scrollbar-thumb {
                    background: rgba(231, 76, 60, 0.5);
                    border-radius: 3px;
                }
                
                .alerts-container::-webkit-scrollbar-thumb:hover {
                    background: rgba(231, 76, 60, 0.7);
                }
            </style>
            
            <div class="alerts-container">
                <div class="header">
                    <div class="header-content">
                        <div class="title">
                            <div class="title-icon">⚠️</div>
                            <div class="title-text">
                                <h3>Global Alerts</h3>
                                <p>Disaster Monitoring</p>
                            </div>
                        </div>
                        <div class="status">
                            <div class="status-dot active"></div>
                            <span>Active</span>
                        </div>
                    </div>
                </div>
                
                <div id="loading" class="loading">
                    <div class="loading-spinner"></div>
                    <p>Loading alerts...</p>
                </div>
                
                <div id="error" class="error" style="display: none;">
                    <p>Failed to load alerts</p>
                    <button class="retry-btn" onclick="this.getRootNode().host.loadData()">Retry</button>
                </div>
                
                <div id="content" style="display: none;">
                    <div id="alerts-list" class="alerts-list"></div>
                    
                    <div id="no-alerts" class="no-alerts" style="display: none;">
                        <div class="no-alerts-icon">🛡️</div>
                        <h3 style="margin: 0 0 8px 0; font-size: 14px; color: #2ecc71;">All Clear</h3>
                        <p style="margin: 0; font-size: 12px;">No active disaster alerts</p>
                    </div>
                </div>
                
                <div class="footer">
                    🛰️ Data from NASA & Global Monitoring Systems
                </div>
            </div>
        `;
    }

    async loadData() {
        const loading = this.shadowRoot.getElementById('loading');
        const error = this.shadowRoot.getElementById('error');
        const content = this.shadowRoot.getElementById('content');
        const statusDot = this.shadowRoot.querySelector('.status-dot');

        try {
            loading.style.display = 'block';
            error.style.display = 'none';
            content.style.display = 'none';

            const response = await fetch('/api/alerts');
            const data = await response.json();

            if (response.ok) {
                this.data = data;
                this.updateDisplay();
                
                loading.style.display = 'none';
                content.style.display = 'block';
                
                if (data.events && data.events.length > 0) {
                    statusDot.className = 'status-dot active';
                } else {
                    statusDot.className = 'status-dot clear';
                }
            } else {
                throw new Error('Failed to fetch alerts data');
            }
        } catch (err) {
            console.error('Alerts widget error:', err);
            loading.style.display = 'none';
            error.style.display = 'block';
            statusDot.className = 'status-dot offline';
        }
    }

    updateDisplay() {
        if (!this.data) return;

        const alertsList = this.shadowRoot.getElementById('alerts-list');
        const noAlerts = this.shadowRoot.getElementById('no-alerts');

        if (this.data.events && this.data.events.length > 0) {
            alertsList.innerHTML = '';
            noAlerts.style.display = 'none';

            this.data.events.forEach((event, index) => {
                const alertElement = this.createAlertElement(event, index);
                alertsList.appendChild(alertElement);
            });
        } else {
            alertsList.innerHTML = '';
            noAlerts.style.display = 'block';
        }
    }

    createAlertElement(event, index) {
        const alertElement = document.createElement('div');
        alertElement.className = 'alert-item';
        alertElement.style.animationDelay = `${index * 0.1}s`;

        alertElement.innerHTML = `
            <div class="alert-header">
                <div class="alert-icon">🔥</div>
                <div class="alert-title">${this.escapeHtml(event.title)}</div>
                <div class="alert-pulse"></div>
            </div>
            <div class="alert-content">
                <div class="alert-detail">
                    <div class="detail-icon category-icon">🏷️</div>
                    <span class="detail-label">Category:</span>
                    <span class="detail-value category-value">${this.escapeHtml(event.category)}</span>
                </div>
                <div class="alert-detail">
                    <div class="detail-icon date-icon">📅</div>
                    <span class="detail-label">Date:</span>
                    <span class="detail-value date-value">${this.escapeHtml(event.date)}</span>
                </div>
                <div class="alert-detail">
                    <div class="detail-icon location-icon">📍</div>
                    <span class="detail-label">Location:</span>
                    <span class="detail-value location-value">${this.escapeHtml(event.coordinates)}</span>
                </div>
            </div>
        `;

        return alertElement;
    }

    startAutoUpdate() {
        // Update every 2 minutes
        this.updateInterval = setInterval(() => {
            this.loadData();
        }, 120000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Register the custom element
customElements.define('alerts-widget', AlertsWidget);