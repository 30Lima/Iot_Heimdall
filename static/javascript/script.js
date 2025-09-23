// IDs dos elementos HTML
const totalMotosEl = document.getElementById("total-motos");
const vagasOcupadasEl = document.getElementById("vagas-ocupadas");
const corretasEl = document.getElementById("corretas");
const logsBody = document.getElementById("logs-body");
const motosErradasPatioEl = document.getElementById("motos-erradas-patio"); // novo card
const motosErradasSaidaEl = document.getElementById("motos-erradas-saida"); // novo card

// ... [configuração dos gráficos Chart.js permanece igual] ...

// Função para atualizar dashboard
async function fetchLogs() {
    try {
        const response = await fetch("/logs");
        const data = await response.json();

        // Atualiza tabela de logs (últimos 20)
        logsBody.innerHTML = "";
        const motosErradasPatio = [];
        const motosErradasSaida = [];

        data.slice(-20).forEach(log => {
            const date = new Date(log.timestamp);
            const formattedTime = date.toLocaleString();

            // Preenche os arrays apenas com IDs das motos erradas
            if (!log.correct && log.status === "entrada") motosErradasPatio.push(log.moto_id);
            if (!log.correct && log.status === "saida") motosErradasSaida.push(log.moto_id);

            // Cria linha da tabela sem exibir status
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${log.moto_id}</td>
                <td>${log.zona}</td>
                <td>${log.vaga}</td>
                <td>${formattedTime}</td>
            `;
            if (!log.correct && log.status === "entrada") tr.classList.add("moto-errada");
            logsBody.appendChild(tr);
        });

        // Função para limitar e formatar lista de motos (só IDs)
        const formatList = list => {
            let display = list.slice(0, 5).join(", ");
            if (list.length > 5) display += " ...";
            return display || "Nenhuma";
        };

        // Atualiza cards com tooltip mostrando todos os IDs
        if (motosErradasPatioEl) {
            motosErradasPatioEl.textContent = formatList(motosErradasPatio);
            motosErradasPatioEl.title = motosErradasPatio.join("\n") || "Nenhuma";
        }
        if (motosErradasSaidaEl) {
            motosErradasSaidaEl.textContent = formatList(motosErradasSaida);
            motosErradasSaidaEl.title = motosErradasSaida.join("\n") || "Nenhuma";
        }

        // Atualiza cards principais
        const entradas = data.filter(log => log.status === "entrada");
        totalMotosEl.textContent = entradas.length;
        vagasOcupadasEl.textContent = entradas.length;
        const corretasCount = entradas.filter(log => log.correct).length;
        corretasEl.textContent = entradas.length > 0 ? `${Math.round((corretasCount / entradas.length) * 100)}%` : "0%";

        // Atualiza gráficos
        chartEntrada.data.datasets[0].data = [entradas.length, data.filter(log => log.status === "saida").length];
        chartCorrect.data.datasets[0].data = [corretasCount, motosErradasPatio.length];
        chartCorrect.update();
        chartEntrada.update();

    } catch (error) {
        console.error("Erro ao buscar logs:", error);
    }
}

// Atualiza dashboard a cada 2 segundos
setInterval(fetchLogs, 2000);
fetchLogs();
