// IDs dos elementos HTML
const totalMotosEl = document.getElementById("total-motos");
const vagasOcupadasEl = document.getElementById("vagas-ocupadas");
const corretasEl = document.getElementById("corretas");
const logsBody = document.getElementById("logs-body");

// Configuração dos gráficos Chart.js
let chartCorrectCtx = document.getElementById("chart-correct").getContext("2d");
let chartEntradaCtx = document.getElementById("chart-entrada").getContext("2d");

let chartCorrect = new Chart(chartCorrectCtx, {
    type: 'doughnut',
    data: {
        labels: ["Corretas", "Erradas"],
        datasets: [{
            data: [0, 0],
            backgroundColor: ['#4caf50', '#f44336']
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { position: 'top' } }
    }
});

let chartEntrada = new Chart(chartEntradaCtx, {
    type: 'bar',
    data: {
        labels: ["Entrada", "Saída"],
        datasets: [{
            label: 'Quantidade',
            data: [0, 0],
            backgroundColor: ['#2196f3', '#ff9800']
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
    }
});

// Função para atualizar dashboard
async function fetchLogs() {
    try {
        const response = await fetch("/logs");
        const data = await response.json();

        // Atualiza tabela de logs (últimos 20)
        logsBody.innerHTML = "";
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
            logsBody.appendChild(tr);
        });

        // Atualiza cards
        totalMotosEl.textContent = data.length;
        vagasOcupadasEl.textContent = data.filter(log => log.status === "entrada").length;
        let corretas = data.filter(log => log.correct).length;
        corretasEl.textContent = data.length > 0 ? `${Math.round((corretas / data.length) * 100)}%` : "0%";

        // Atualiza gráficos
        chartCorrect.data.datasets[0].data = [corretas, data.length - corretas];

        let entradas = data.filter(log => log.status === "entrada").length;
        let saidas = data.filter(log => log.status === "saida").length;
        chartEntrada.data.datasets[0].data = [entradas, saidas];

        chartCorrect.update();
        chartEntrada.update();

    } catch (error) {
        console.error("Erro ao buscar logs:", error);
    }
}

// Atualiza dashboard a cada 2 segundos
setInterval(fetchLogs, 2000);
fetchLogs();
