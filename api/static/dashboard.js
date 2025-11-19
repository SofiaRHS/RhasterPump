let interval = "1m";

function showInterval(i){
    interval = i;
}

async function fetchData(){
    const res = await fetch("/data");
    const data = await res.json();
    const container = document.getElementById("cards");
    container.innerHTML = "";
    for(const key in data.price_data){
        if(!key.endsWith(interval)) continue;
        const item = data.price_data[key];
        const signal = data.signals[key];
        const card = document.createElement("div");
        card.className = "card";
        card.style.border = `2px solid ${signal=="pump"?"green":signal=="drop"?"red":"gray"}`;
        card.innerHTML = `<h3>${key.split("@")[0]}</h3>
                          <p>Close: ${item.close}</p>
                          <p>Change: ${item.percent?.toFixed(2) || 0}%</p>`;
        container.appendChild(card);
    }
}

setInterval(fetchData, 3000);
