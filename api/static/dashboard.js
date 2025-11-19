async function fetchData() {
    const res = await fetch("/data");
    const data = await res.json();
    const table = document.getElementById("pairs-table");
    table.innerHTML = "";

    for (const key in data.price_data) {
        const row = document.createElement("tr");
        const v = data.price_data[key];
        const signal = data.signals[key];
        row.innerHTML = `
            <td>${key}</td>
            <td>${v.close}</td>
            <td style="color:${signal=="pump"?"green":signal=="drop"?"red":"black"}">${signal}</td>
        `;
        table.appendChild(row);
    }
}

setInterval(fetchData, 5000);
