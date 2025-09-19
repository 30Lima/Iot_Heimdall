async function fetchLogs() {
    try {
        const response = await fetch("/logs");
        const data = await response.json();
        const tbody = document.getElementById("logs-body");
        tbody.innerHTML = "";

        data.slice(-20).forEach(log => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${log.moto_id}</td>
                <td>${log.zona}</td>
                <td>${log.vaga}</td>
                <td>${log.status}</td>
                <td>${log.correct}</td>
                <td>${log.timestamp}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Erro ao buscar logs:", err);
    }
}

setInterval(fetchLogs, 2000);
fetchLogs();
