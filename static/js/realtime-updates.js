/**
 * Real-time Updates using Server-Sent Events (SSE)
 * Alternative to iframes for live data updates
 */

class RealtimeUpdates {
    constructor() {
        this.weatherEventSource = null;
        this.alertsEventSource = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000; // Start with 1 second
    }

    // Initialize real-time updates
    init() {
        this.setupWeatherUpdates();
        this.setupAlertsUpdates();
        this.setupVisibilityHandling();
    }

    // Setup weather updates via SSE
    setupWeatherUpdates() {
        if (typeof(EventSource) !== "undefined") {
            this.weatherEventSource = new EventSource('/api/weather/stream');
            
            this.weatherEventSource.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.updateWeatherDisplay(data);
                    this.reconnectAttempts = 0; // Reset on successful connection
                } catch (error) {
                    console.error('Error parsing weather data:', error);
                }
            };

            this.weatherEventSource.onerror = (error) => {
                console.error('Weather SSE error:', error);
                this.handleWeatherReconnect();
            };
        } else {
            // Fallback to polling for older browsers
            this.startWeatherPolling();
        }
    }

    // Setup alerts updates via SSE
    setupAlertsUpdates() {
        if (typeof(EventSource) !== "undefined") {
            this.alertsEventSource = new EventSource('/api/alerts/stream');
            
            this.alertsEventSource.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.updateAlertsDisplay(data);
                    this.reconnectAttempts = 0; // Reset on successful connection
                } catch (error) {
                    console.error('Error parsing alerts data:', error);
                }
            };

            this.alertsEventSource.onerror = (error) => {
                console.error('Alerts SSE error:', error);
                this.handleAlertsReconnect();
            };
        } else {
            // Fallback to polling for older browsers
            this.startAlertsPolling();
        }
    }

    // Update weather display
    updateWeatherDisplay(data) {
        const elements = {
            temperature: document.getElementById('temperature'),
            windspeed: document.getElementById('windspeed'),
            winddirection: document.getElementById('winddirection'),
            weatherTime: document.getElementById('weather-time'),
            compass: document.getElementById('compass'),
            weatherStatus: document.getElementById('weather-status')
        };

        if (elements.temperature) elements.temperature.textContent = `${data.temperature}°`;
        if (elements.windspeed) elements.windspeed.textContent = `${data.windspeed} km/h`;
        if (elements.winddirection) elements.winddirection.textContent = `${data.winddirection}°`;
        if (elements.weatherTime) elements.weatherTime.textContent = data.time;
        if (elements.compass) elements.compass.style.transform = `rotate(${data.winddirection}deg)`;
        
        // Update status indicator
        if (elements.weatherStatus) {
            elements.weatherStatus.className = 'w-2 h-2 bg-green-500 rounded-full animate-pulse';
        }

        // Show data, hide loading
        const loading = document.getElementById('weather-loading');
        const dataDiv = document.getElementById('weather-data');
        if (loading) loading.classList.add('hidden');
        if (dataDiv) dataDiv.classList.remove('hidden');

        // Add update animation
        this.addUpdateAnimation('weather-container');
    }

    // Update alerts display
    updateAlertsDisplay(data) {
        const alertsContainer = document.getElementById('alerts-data');
        const loading = document.getElementById('alerts-loading');
        const noAlerts = document.getElementById('no-alerts');
        const alertsStatus = document.getElementById('alerts-status');

        if (!alertsContainer) return;

        if (data.events && data.events.length > 0) {
            // Clear existing content
            alertsContainer.innerHTML = '';
            
            // Add each alert with animation
            data.events.forEach((event, index) => {
                const alertElement = this.createAlertElement(event, index);
                alertsContainer.appendChild(alertElement);
                
                // Animate in
                setTimeout(() => {
                    alertElement.style.opacity = '1';
                    alertElement.style.transform = 'translateY(0)';
                }, index * 100);
            });
            
            // Show alerts data
            alertsContainer.parentElement.classList.remove('hidden');
            if (noAlerts) noAlerts.classList.add('hidden');
            
        } else {
            // Show no alerts state
            if (noAlerts) noAlerts.classList.remove('hidden');
            alertsContainer.parentElement.classList.add('hidden');
        }
        
        // Hide loading, update status
        if (loading) loading.classList.add('hidden');
        if (alertsStatus) {
            alertsStatus.className = 'w-2 h-2 bg-green-500 rounded-full animate-pulse';
        }

        // Add update animation
        this.addUpdateAnimation('alerts-container');
    }

    // Create alert element
    createAlertElement(event, index) {
        const alertElement = document.createElement('div');
        alertElement.className = 'bg-white rounded-xl border border-red-200 overflow-hidden shadow-sm hover:shadow-md transition-all duration-300 opacity-0 transform translate-y-4';
        alertElement.style.transitionDelay = `${index * 50}ms`;
        
        alertElement.innerHTML = `
            <div class="bg-gradient-to-r from-red-500 to-orange-500 p-2 text-white">
                <div class="flex items-center space-x-2">
                    <div class="w-5 h-5 bg-white/20 rounded-lg flex items-center justify-center">
                        <i class="fas fa-fire text-xs"></i>
                    </div>
                    <h3 class="font-bold text-xs leading-tight flex-1">${this.escapeHtml(event.title)}</h3>
                    <div class="w-1.5 h-1.5 bg-yellow-400 rounded-full animate-pulse"></div>
                </div>
            </div>
            <div class="p-2 space-y-1">
                <div class="flex items-center space-x-2">
                    <i class="fas fa-tag text-blue-500 text-xs"></i>
                    <span class="text-xs text-gray-600">Category:</span>
                    <span class="text-xs text-blue-600 font-semibold">${this.escapeHtml(event.category)}</span>
                </div>
                <div class="flex items-center space-x-2">
                    <i class="fas fa-calendar text-green-500 text-xs"></i>
                    <span class="text-xs text-gray-600">Date:</span>
                    <span class="text-xs text-green-600 font-semibold">${this.escapeHtml(event.date)}</span>
                </div>
                <div class="flex items-center space-x-2">
                    <i class="fas fa-map-marker-alt text-purple-500 text-xs"></i>
                    <span class="text-xs text-gray-600">Location:</span>
                    <span class="text-xs text-purple-600 font-semibold">${this.escapeHtml(event.coordinates)}</span>
                </div>
            </div>
        `;
        
        return alertElement;
    }

    // Handle weather reconnection
    handleWeatherReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
            
            setTimeout(() => {
                console.log(`Attempting to reconnect weather stream (attempt ${this.reconnectAttempts})`);
                this.setupWeatherUpdates();
            }, delay);
        } else {
            console.error('Max reconnection attempts reached for weather stream');
            this.startWeatherPolling(); // Fallback to polling
        }
    }

    // Handle alerts reconnection
    handleAlertsReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
            
            setTimeout(() => {
                console.log(`Attempting to reconnect alerts stream (attempt ${this.reconnectAttempts})`);
                this.setupAlertsUpdates();
            }, delay);
        } else {
            console.error('Max reconnection attempts reached for alerts stream');
            this.startAlertsPolling(); // Fallback to polling
        }
    }

    // Fallback polling for weather
    startWeatherPolling() {
        const pollWeather = async () => {
            try {
                const response = await fetch('/api/weather');
                const data = await response.json();
                this.updateWeatherDisplay(data);
            } catch (error) {
                console.error('Weather polling error:', error);
            }
        };

        // Poll every 30 seconds
        setInterval(pollWeather, 30000);
        pollWeather(); // Initial load
    }

    // Fallback polling for alerts
    startAlertsPolling() {
        const pollAlerts = async () => {
            try {
                const response = await fetch('/api/alerts');
                const data = await response.json();
                this.updateAlertsDisplay(data);
            } catch (error) {
                console.error('Alerts polling error:', error);
            }
        };

        // Poll every 60 seconds
        setInterval(pollAlerts, 60000);
        pollAlerts(); // Initial load
    }

    // Handle page visibility changes
    setupVisibilityHandling() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                // Page is hidden, close connections to save resources
                this.closeConnections();
            } else {
                // Page is visible again, reconnect
                this.init();
            }
        });
    }

    // Close all connections
    closeConnections() {
        if (this.weatherEventSource) {
            this.weatherEventSource.close();
            this.weatherEventSource = null;
        }
        if (this.alertsEventSource) {
            this.alertsEventSource.close();
            this.alertsEventSource = null;
        }
    }

    // Add visual update animation
    addUpdateAnimation(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.classList.add('animate-pulse');
            setTimeout(() => {
                container.classList.remove('animate-pulse');
            }, 500);
        }
    }

    // Escape HTML to prevent XSS
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Cleanup on page unload
    cleanup() {
        this.closeConnections();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const realtimeUpdates = new RealtimeUpdates();
    realtimeUpdates.init();
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        realtimeUpdates.cleanup();
    });
});