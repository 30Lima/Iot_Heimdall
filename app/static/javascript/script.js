document.addEventListener('DOMContentLoaded', () => {

    const totalMotosEl = document.getElementById("total-motos");
    const vagasOcupadasEl = document.getElementById("vagas-ocupadas");
    const corretasEl = document.getElementById("corretas");
    const logsBody = document.getElementById("logs-body");
    const motosErradasPatioEl = document.getElementById("motos-erradas-patio");

    const ctxBar = document.getElementById("chart-entrada").getContext("2d");
    const ctxPie = document.getElementById("chart-correct").getContext("2d");

    const patioGridEl = document.getElementById("patio-grid");

    let barChart, pieChart;

    const VAGAS_DO_PATIO = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'
    ];

    function initializeCharts() {
        barChart = new Chart(ctxBar, {
            type: "bar",
            data: {
                labels: ["ZC1", "ZC2", "ZE"],
                datasets: [{
                    label: "Entradas por Zona",
                    data: [0, 0, 0],
                    backgroundColor: ["#ff6384", "#36a2eb", "#ffce56"],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
            }
        });

        pieChart = new Chart(ctxPie, {
            type: "pie",
            data: {
                labels: ["Corretas", "Incorretas"],
                datasets: [{
                    data: [0, 0],
                    backgroundColor: ["#4caf50", "#f44336"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }


    function initializePatio() {
        if (!patioGridEl) return;

        VAGAS_DO_PATIO.forEach(idVaga => {
            const vagaEl = document.createElement('div');
            vagaEl.id = `vaga-${idVaga}`;
            vagaEl.classList.add('vaga', 'livre');
            vagaEl.textContent = idVaga;
            patioGridEl.appendChild(vagaEl);
        });
    }

    async function updateDashboard() {
        try {
            await Promise.all([
                updateLogsAndCharts(),
                updatePatioStatus()
            ]);

        } catch (error) {
            console.error("❌ Erro ao orquestrar o dashboard:", error);
        }
    }

    async function updateLogsAndCharts() {
        try {
            const response = await fetch("/logs");
            if (!response.ok) throw new Error(`Erro na API /logs: ${response.statusText}`);
            const data = await response.json();

            const motosErradasPatio = [];
            const zones = ["ZC1", "ZC2", "ZE"];
            const entriesPerZone = { "ZC1": 0, "ZC2": 0, "ZE": 0 };
            let correctCount = 0;
            let incorrectCount = 0;

            const graphData = data.slice(-50);
            graphData.forEach(log => {
                if (zones.includes(log.zona)) entriesPerZone[log.zona]++;
                if (log.correct) correctCount++;
                else incorrectCount++;
            });

            const entradas = data.filter(log => log.status === "entrada");
            const corretasCountKPI = entradas.filter(log => log.correct).length;

            const tableData = data.slice(-20).reverse();
            logsBody.innerHTML = "";

            tableData.forEach(log => {
                const date = new Date(log.timestamp);
                const formattedTime = date.toLocaleString('pt-BR');

                if (!log.correct && log.status === "entrada") {
                    motosErradasPatio.push(log.moto_id);
                }

                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${log.moto_id}</td>
                    <td>${log.zona}</td>
                    <td>${log.vaga}</td>
                    <td>${formattedTime}</td>
                `;
                if (!log.correct && log.status === "entrada") {
                    tr.classList.add("moto-errada");
                }
                logsBody.appendChild(tr);
            });

            totalMotosEl.textContent = entradas.length;
            corretasEl.textContent = entradas.length > 0 ? `${Math.round((corretasCountKPI / entradas.length) * 100)}%` : "0%";

            const formatList = list => {
                let display = [...new Set(list)].slice(0, 5).join(", ");
                if (list.length > 5) display += " ...";
                return display || "Nenhuma";
            };
            motosErradasPatioEl.textContent = formatList(motosErradasPatio);
            motosErradasPatioEl.title = [...new Set(motosErradasPatio)].join("\n") || "Nenhuma";

            barChart.data.datasets[0].data = zones.map(z => entriesPerZone[z]);
            pieChart.data.datasets[0].data = [correctCount, incorrectCount];
            barChart.update();
            pieChart.update();

        } catch (error) {
            console.error("❌ Erro ao atualizar logs e gráficos:", error);
        }
    }

    async function updatePatioStatus() {
        try {
            const response = await fetch("/api/patio/status");
            if (!response.ok) throw new Error(`Erro na API /api/patio/status: ${response.statusText}`);

            const vagasOcupadas = await response.json();

            vagasOcupadasEl.textContent = vagasOcupadas.length;

            const mapaVagas = new Map();
            vagasOcupadas.forEach(item => {
                mapaVagas.set(item.vaga, item.moto_id);
            });

            VAGAS_DO_PATIO.forEach(idVaga => {
                const vagaEl = document.getElementById(`vaga-${idVaga}`);
                if (!vagaEl) return;

                if (mapaVagas.has(idVaga)) {
                    const motoID = mapaVagas.get(idVaga);
                    vagaEl.classList.replace('livre', 'ocupada');
                    vagaEl.setAttribute('data-moto-id', motoID);
                } else {
                    vagaEl.classList.replace('ocupada', 'livre');
                    vagaEl.removeAttribute('data-moto-id');
                }
            });

        } catch (error) {
            console.error("❌ Erro ao atualizar o status do pátio:", error);
        }
    }

    initializeCharts();
    initializePatio();
    updateDashboard();
    setInterval(updateDashboard, 2000);

});