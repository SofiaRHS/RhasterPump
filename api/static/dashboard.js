let timeframe = '1m';

function fetchSignals() {
    fetch(`/signals?tf=${timeframe}`)
        .then(res => res.json())
        .then(data => renderDashboard(data));
}

function renderDashboard(pairs) {
    const container = document.getElementById("dashboard");
    container.innerHTML = "";
    pairs.forEach(p => {
        const card = document.createElement("div");
        card.className = "card " + p.trend;
        card.innerHTML = `<h3>${p.pair}</h3><p>${p.percent}%</p><div id="chart-${p.pair}"></div>`;
        container.appendChild(card);

        let options = {
            chart: { type: 'line', height: 100 },
            series: [{ data: [p.percent] }],
            xaxis: { categories: [0] }
        };
        new ApexCharts(document.querySelector(`#chart-${p.pair}`), options).render();
    });
}

function setTF(tf) {
    timeframe = tf;
    fetchSignals();
}

function addPair() {
    const pair = document.getElementById("newPair").value;
    fetch('/add_pair', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({pair})
    }).then(() => fetchSignals());
}

setInterval(fetchSignals, 2000);
fetchSignals();
