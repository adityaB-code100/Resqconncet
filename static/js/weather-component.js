/**
 * Weather Web Component
 * Modern alternative to iframes using Web Components
 */

class WeatherWidget extends HTMLElement {
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
                
                .weather-container {
                    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%);
                    backdrop-filter: blur(20px);
                    border: 1px solid rgba(255,255,255,0.3);
                    border-radius: 16px;
                    padding: 16px;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                }
                
                .header {
                    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 50%, #6c5ce7 100%);
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
                
                .location {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                
                .location-icon {
                    width: 32px;
                    height: 32px;
                    background: rgba(255,255,255,0.2);
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    backdrop-filter: blur(10px);
                }
                
                .location-text h3 {
                    margin: 0;
                    font-size: 16px;
                    font-weight: bold;
                }
                
                .location-text p {
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
                
                .status-dot.online {
                    background: #00b894;
                }
                
                .status-dot.offline {
                    background: #e17055;
                }
                
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
                
                .data-grid {
                    display: grid;
                    gap: 12px;
                }
                
                .data-item {
                    background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(248,250,252,0.8) 100%);
                    border: 1px solid rgba(0,0,0,0.1);
                    border-radius: 12px;
                    padding: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    transition: all 0.3s ease;
                }
                
                .data-item:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                }
                
                .data-left {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }
                
                .data-icon {
                    width: 32px;
                    height: 32px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 12px;
                }
                
                .temp-icon { background: linear-gradient(135deg, #fd79a8, #e84393); }
                .wind-icon { background: linear-gradient(135deg, #00b894, #00cec9); }
                .direction-icon { background: linear-gradient(135deg, #a29bfe, #6c5ce7); }
                
                .data-label {
                    font-size: 12px;
                    color: #666;
                }
                
                .data-value {
                    text-align: right;
                }
                
                .data-value .value {
                    font-size: 18px;
                    font-weight: bold;
                    margin: 0;
                }
                
                .data-value .unit {
                    font-size: 10px;
                    color: #888;
                }
                
                .temp-value { color: #e84393; }
                .wind-value { color: #00b894; }
                .direction-value { color: #6c5ce7; }
                
                .footer {
                    margin-top: 16px;
                    padding-top: 12px;
                    border-top: 1px solid rgba(0,0,0,0.1);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    font-size: 11px;
                    color: #666;
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
                    border-top: 3px solid #4A90E2;
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
                    background: #4A90E2;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 12px;
                    margin-top: 8px;
                }
                
                .retry-btn:hover {
                    background: #357ABD;
                }
            </style>
            
            <div class="weather-container">
                <div id="loading" class="loading">
                    <div class="loading-spinner"></div>
                    <p>Loading weather data...</p>
                </div>
                
                <div id="error" class="error" style="display: none;">
                    <p>Failed to load weather data</p>
                    <button class="retry-btn" onclick="this.getRootNode().host.loadData()">Retry</button>
                </div>
                
                <div id="content" style="display: none;">
                    <div class="header">
                        <div class="header-content">
                            <div class="location">
                                <div class="location-icon">📍</div>
                                <div class="location-text">
                                    <h3>New Delhi</h3>
                                    <p>India's Capital</p>
                                </div>
                            </div>
                            <div class="status">
                                <div class="status-dot online"></div>
                                <span>Live</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="data-grid">
                        <div class="data-item">
                            <div class="data-left">
                                <div class="data-icon temp-icon">🌡️</div>
                                <div class="data-label">Temperature</div>
                            </div>
                            <div class="data-value">
                                <div class="value temp-value" id="temperature">--°</div>
                                <div class="unit">Celsius</div>
                            </div>
                        </div>
                        
                        <div class="data-item">
                            <div class="data-left">
                                <div class="data-icon wind-icon">💨</div>
                                <div class="data-label">Wind Speed</div>
                            </div>
                            <div class="data-value">
                                <div class="value wind-value" id="windspeed">-- km/h</div>
                            </div>
                        </div>
                        
                        <div class="data-item">
                            <div class="data-left">
                                <div class="data-icon direction-icon" id="compass">🧭</div>
                                <div class="data-label">Direction</div>
                            </div>
                            <div class="data-value">
                                <div class="value direction-value" id="winddirection">--°</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <span>🕒 Last updated</span>
                        <span id="weather-time">--</span>
                    </div>
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

            const response = await fetch('/api/weather');
            const data = await response.json();

            if (response.ok) {
                this.data = data;
                this.updateDisplay();
                
                loading.style.display = 'none';
                content.style.display = 'block';
                statusDot.className = 'status-dot online';
            } else {
                throw new Error('Failed to fetch weather data');
            }
        } catch (err) {
            console.error('Weather widget error:', err);
            loading.style.display = 'none';
            error.style.display = 'block';
            statusDot.className = 'status-dot offline';
        }
    }

    updateDisplay() {
        if (!this.data) return;

        const elements = {
            temperature: this.shadowRoot.getElementById('temperature'),
            windspeed: this.shadowRoot.getElementById('windspeed'),
            winddirection: this.shadowRoot.getElementById('winddirection'),
            weatherTime: this.shadowRoot.getElementById('weather-time'),
            compass: this.shadowRoot.getElementById('compass')
        };

        if (elements.temperature) elements.temperature.textContent = `${this.data.temperature}°`;
        if (elements.windspeed) elements.windspeed.textContent = `${this.data.windspeed} km/h`;
        if (elements.winddirection) elements.winddirection.textContent = `${this.data.winddirection}°`;
        if (elements.weatherTime) elements.weatherTime.textContent = this.data.time;
        if (elements.compass) {
            elements.compass.style.transform = `rotate(${this.data.winddirection}deg)`;
        }
    }

    startAutoUpdate() {
        // Update every 5 minutes
        this.updateInterval = setInterval(() => {
            this.loadData();
        }, 300000);
    }
}

// Register the custom element
customElements.define('weather-widget', WeatherWidget);