let stockChart;
const API_BASE_URL = 'https://market-dashboard-gun5.onrender.com';
document.getElementById('searchBtn').addEventListener('click', async () => {
    const tickerInput = document.getElementById('tickerInput');
    const ticker = tickerInput.value.toUpperCase();
    const container = document.getElementById('resultContainer');

    if (!ticker) {
        alert("COMMAND ERROR: TICKER REQUIRED");
        return;
    }

    container.innerHTML = `<p>EXECUTING DATA FETCH FOR [${ticker}]...</p>`;

    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/${ticker}`);
        
        if (!response.ok) throw new Error('STATION OFFLINE');

        const data = await response.json();
        loadChart(ticker);

        // Build the News Feed
        const newsHtml = data.news.map(item => {
            const title = (item.title || item.headline || 'N/A').toUpperCase();
            const source = (item.source || 'INTEL').toUpperCase();
            const sentiment = (item.sentiment || 'NEUTRAL').toUpperCase();
            
            // Color code sentiment
            let sentColor = 'var(--terminal-amber)';
            if(sentiment.includes('BULLISH') || sentiment.includes('POSITIVE')) sentColor = 'var(--terminal-green)';
            if(sentiment.includes('BEARISH') || sentiment.includes('NEGATIVE')) sentColor = 'var(--terminal-red)';

            return `
                <div style="border-bottom: 1px solid #222; padding: 8px 0; font-size: 0.9em;">
                    <a href="${item.url}" target="_blank" style="color: var(--terminal-blue); text-decoration: none;">
                        > ${title}
                    </a>
                    <div style="margin-top: 4px; color: #888;">
                        SRC: ${source} | <span style="color: ${sentColor}">SENTIMENT: ${sentiment}</span>
                    </div>
                </div>
            `;
        }).join('');

        // Build Terminal Output
        container.innerHTML = `
            <div class="card">
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--terminal-amber); padding-bottom: 5px;">
                    <span style="font-size: 1.5em; font-weight: bold;">EQUITY: ${ticker}</span>
                    <span style="font-size: 1.5em; color: var(--terminal-green);">
                        USD ${Number(data.stock.price).toFixed(2)}
                    </span>
                </div>
                
                <div style="margin-top: 15px;">
                    <div style="background: var(--terminal-amber); color: black; padding: 2px 5px; display: inline-block; font-weight: bold; margin-bottom: 10px;">
                        HEADLINES
                    </div>
                    <div class="news-list">
                        ${newsHtml || '<p>NO DATA AVAILABLE FOR THIS FEED</p>'}
                    </div>
                </div>
            </div>
        `;
        await loadChart(ticker);

    } catch (error) {
        container.innerHTML = `
            <div style="border: 1px solid var(--terminal-red); padding: 20px; color: var(--terminal-red);">
                <p><strong>>> SYSTEM ERROR: UNABLE TO REACH SERVER</strong></p>
                <p>STATUS: 500 - CONNECTION_REFUSED</p>
            </div>
        `;
    }
});
async function loadChart(ticker) {

    const response = await fetch(`${API_BASE_URL}/stock/history/${ticker}`);

    const historyData = await response.json();

    const ctx = document.getElementById('stockChart');
    if (!ctx) return;
    // destroy old chart
    if (stockChart) {
        stockChart.destroy();
    }

    stockChart = new Chart(ctx, {

        type: 'line',

        data: {

            labels: historyData.dates,

            datasets: [{
                label: `${ticker} PRICE`,
                data: historyData.prices,

                borderColor: '#00ff00',

                backgroundColor: 'rgba(0,255,0,0.1)',

                tension: 0.2
            }]
        },

        options: {

            responsive: true,

            plugins: {
                legend: {
                    labels: {
                        color: '#ffb000'
                    }
                }
            },

            scales: {

                x: {
                    ticks: {
                        color: '#ffb000'
                    },

                    grid: {
                        color: '#222'
                    }
                },

                y: {
                    ticks: {
                        color: '#00ff00'
                    },

                    grid: {
                        color: '#222'
                    }
                }
            }
        }
    });
} 