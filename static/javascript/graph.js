async function fetchAndDrawGraphs() {
    try {
        const response = await fetch("/logs");
        const data = await response.json();

        // --- Agrupando dados ---
        const zones = ["ZC1", "ZC2", "ZE"];
        const entriesPerZone = { "ZC1": 0, "ZC2": 0, "ZE": 0 };
        let correctCount = 0;
        let incorrectCount = 0;

        data.slice(-50).forEach(log => { // pegando apenas os últimos 50 logs
            if (zones.includes(log.zona)) entriesPerZone[log.zona]++;
            if (log.correct) correctCount++;
            else incorrectCount++;
        });

        // --- Gráfico de barras: Entradas por Zona ---
        const ctxBar = document.getElementById("chart-entrada").getContext("2d");
        if (window.barChart) window.barChart.destroy(); // destrói gráfico anterior
        window.barChart = new Chart(ctxBar, {
            type: "bar",
            data: {
                labels: zones,
                datasets: [{
                    label: "Entradas por Zona",
                    data: zones.map(z => entriesPerZone[z]),
                    backgroundColor: ["#ff6384", "#36a2eb", "#ffce56"],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });

        // --- Gráfico de pizza: Corretas vs Incorretas ---
        const ctxPie = document.getElementById("chart-correct").getContext("2d");
        if (window.pieChart) window.pieChart.destroy(); // destrói gráfico anterior
        window.pieChart = new Chart(ctxPie, {
            type: "pie",
            data: {
                labels: ["Corretas", "Incorretas"],
                datasets: [{
                    data: [correctCount, incorrectCount],
                    backgroundColor: ["#4caf50", "#f44336"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });

    } catch (err) {
        console.error("Erro ao buscar dados para gráficos:", err);
    }
}

// Atualiza os gráficos a cada 2s
setInterval(fetchAndDrawGraphs, 2000);
fetchAndDrawGraphs();
