const { useState, useEffect, useRef } = React;

function App() {
    const [metrics, setMetrics] = useState(null);
    const chartRef = useRef(null);
    const chartInstance = useRef(null);

    // 1. Data Fetching Loop
    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const res = await fetch("/api/metrics");
                const data = await res.json();
                setMetrics(data);
            } catch (err) {
                console.error("Fetch error:", err);
            }
        };

        fetchMetrics();
        const interval = setInterval(fetchMetrics, 1000);
        return () => clearInterval(interval);
    }, []);

    // 2. Chart Initialization and Update
    useEffect(() => {
        // If we don't have the canvas yet, do nothing
        if (!metrics || !chartRef.current) return;

        // Initialize Chart if it doesn't exist yet
        if (!chartInstance.current) {
            const ctx = chartRef.current.getContext('2d');
            chartInstance.current = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: 'Anomaly Score',
                            data: [],
                            borderColor: '#ef4444',
                            backgroundColor: 'rgba(239, 68, 68, 0.2)',
                            fill: true,
                            tension: 0.4,
                            yAxisID: 'y'
                        },
                        {
                            label: 'Writes / Sec',
                            data: [],
                            borderColor: '#3b82f6',
                            backgroundColor: 'transparent',
                            tension: 0.4,
                            yAxisID: 'y1'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: false,
                    scales: {
                        x: { display: false },
                        y: { type: 'linear', display: true, position: 'left', title: { display: true, text: 'Anomaly (0-1)' }, suggestedMin: 0, suggestedMax: 1 },
                        y1: { type: 'linear', display: true, position: 'right', title: { display: true, text: 'Writes/s' }, grid: { drawOnChartArea: false } }
                    },
                    plugins: { legend: { labels: { color: '#fff' } } }
                }
            });
        }

        // Update Chart Data
        if (chartInstance.current && metrics.history) {
            chartInstance.current.data.labels = metrics.history.timestamps.map(t => new Date(t * 1000).toLocaleTimeString());
            chartInstance.current.data.datasets[0].data = metrics.history.scores;
            chartInstance.current.data.datasets[1].data = metrics.history.writes;
            chartInstance.current.update();
        }
    }, [metrics]);

    const handleTrigger = async () => {
        await fetch("/api/trigger", { method: "POST" });
    };

    const handleReset = async () => {
        await fetch("/api/reset", { method: "POST" });
    };

    if (!metrics) {
        return <div className="flex h-screen items-center justify-center text-xl animate-pulse">Initializing API Telemetry Connection...</div>;
    }

    const isCritical = metrics.status === "Ransomware Likely";
    const statusColor = isCritical ? "text-red-500" : (metrics.status === "Suspicious" ? "text-yellow-500" : "text-emerald-500");

    return (
        <div className="flex flex-col gap-6">
            {/* Header */}
            <header className="flex justify-between items-center pb-4 border-b border-gray-700">
                <div>
                    <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
                        Foresight-RX
                    </h1>
                    <p className="text-gray-400 text-sm mt-1">Real-Time ML Ransomware Prediction • AMD ROCm Architecture</p>
                </div>
                <div className="flex gap-4">
                    <button onClick={handleTrigger} className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors shadow-lg shadow-red-500/20">
                        Trigger Attack Simulation
                    </button>
                    <button onClick={handleReset} className="px-4 py-2 glass-panel hover:bg-slate-700 text-white rounded-lg font-medium transition-colors">
                        Reset System State
                    </button>
                </div>
            </header>

            {/* Critical Banner */}
            {isCritical && (
                <div className="p-4 bg-red-900/50 border border-red-500 rounded-lg animate-pulse flex items-center justify-between">
                    <span className="font-bold text-red-200">⚠️ CRITICAL THREAT DETECTED: Anomalous file encryption pattern (Ransomware precursor) identified!</span>
                </div>
            )}

            {/* Metrics Top Row */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className={`p-6 rounded-xl glass-panel flex flex-col ${isCritical ? 'attack-pulse' : ''}`}>
                    <span className="text-gray-400 text-sm font-medium uppercase tracking-wider">System Status</span>
                    <span className={`text-2xl font-bold mt-2 ${statusColor}`}>{metrics.status}</span>
                </div>
                <div className="p-6 rounded-xl glass-panel flex flex-col">
                    <span className="text-gray-400 text-sm font-medium uppercase tracking-wider">AI Anomaly Score</span>
                    <span className="text-3xl font-bold mt-2 text-white">{metrics.anomaly_score}</span>
                </div>
                <div className="p-6 rounded-xl glass-panel flex flex-col">
                    <span className="text-gray-400 text-sm font-medium uppercase tracking-wider">File Writes</span>
                    <span className="text-3xl font-bold mt-2 text-white">{metrics.writes_per_sec} <span className="text-lg text-gray-500">/sec</span></span>
                </div>
                <div className="p-6 rounded-xl glass-panel flex flex-col">
                    <span className="text-gray-400 text-sm font-medium uppercase tracking-wider">CPU Spikes</span>
                    <span className="text-3xl font-bold mt-2 text-white">{metrics.cpu_spike}%</span>
                </div>
            </div>

            {/* Chart Area */}
            <div className="p-6 rounded-xl glass-panel mt-4 flex-1 h-[500px] flex flex-col">
                <h3 className="text-lg font-medium mb-4">Live Telemetry Timeline</h3>
                <div className="relative flex-1 w-full h-full">
                    <canvas ref={chartRef}></canvas>
                </div>
            </div>

            <footer className="text-center text-sm text-gray-500 mt-8">
                Created for the Slingshot Prototype Hackathon • React UI Update
            </footer>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
