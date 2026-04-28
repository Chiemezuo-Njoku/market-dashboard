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
        const response = await fetch(`http://127.0.0.1:8000/dashboard/${ticker}`);
        
        if (!response.ok) throw new Error('STATION OFFLINE');

        const data = await response.json();

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
                        SRC: ${source} | <span style="color: ${sentColor}">SENT: ${sentiment}</span>
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

    } catch (error) {
        container.innerHTML = `
            <div style="border: 1px solid var(--terminal-red); padding: 20px; color: var(--terminal-red);">
                <p><strong>>> SYSTEM ERROR: UNABLE TO REACH SERVER</strong></p>
                <p>STATUS: 500 - CONNECTION_REFUSED</p>
            </div>
        `;
    }
});