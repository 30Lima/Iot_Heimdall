# HEIMDALL - Plataforma de Monitoramento de Pátio
> Solução para o challenge da Mottu promovido pela FIAP (Sprint 4 - Disruptive Architectures)

## Integrantes

| Nome Completo                 | RM      |
|-----------------------------|---------|
| Pedro Henrique Lima Santos  | 558243  |
| Vitor Gomes Martins         | 558244  |
| Leonardo Pimentel Santos    | 557541  |

## 1. Descrição da Solução

O **HEIMDALL** é uma plataforma de monitoramento de pátio em tempo real, construída com uma arquitetura de microsserviços desacoplada. A solução utiliza **Python (Flask)** para o *backend* e **JavaScript** puro para o *frontend*, com um banco de dados **Oracle** como fonte única da verdade.

O objetivo é fornecer à Mottu uma visão clara e instantânea do seu pátio logístico, permitindo o rastreamento de vagas e a identificação de anomalias.

## 2. Arquitetura da Solução

O sistema funciona num fluxo de dados contínuo, de ponta a ponta:

1.  **Captura (IoT):** Um simulador de ESP32 (Wokwi) publica eventos de telemetria (ID da moto, vaga, status) num tópico **MQTT** (`broker.hivemq.com`).
2.  **Ingestão (Backend):** Um *script* (`mqtt_client.py`), a correr num *thread* separado, subscreve ao tópico MQTT, recebe os dados e faz o `INSERT` em tempo real no banco de dados **Oracle** (usando SQLAlchemy).
3.  **Persistência (Banco):** O **Oracle DB** armazena todo o histórico de eventos.
4.  **Consumo (API):** O **Flask** serve uma API REST com dois *endpoints*:
    * `GET /logs`: Retorna o histórico dos últimos 100 eventos (para a tabela de logs e gráficos de tendência).
    * `GET /api/patio/status`: Retorna o **estado atual** do pátio (apenas as vagas ocupadas), usando uma consulta SQL complexa (com `ROW_NUMBER()`) para calcular o último estado de cada vaga.
5.  **Visualização (Frontend):** O *dashboard* (`index.html`) usa JavaScript para consumir os dois *endpoints* a cada 2 segundos, atualizando os KPIs, os gráficos, a tabela de logs e o grid do pátio em tempo real.

## 3. Funcionalidades do Dashboard

* **Visão Geral do Pátio (Grid):** Um mapa modular (feito com CSS Grid) que exibe todas as vagas do pátio e as "pinta" (de verde para amarelo) quando uma moto estaciona, mostrando o ID da moto na vaga.
* **Indicadores (KPIs):** *Cards* que mostram o "Total de Motos Ativas", "Vagas Ocupadas" (com base no estado real) e a "% de Entradas Corretas".
* **Alertas em Tempo Real:** Um *card* que lista os IDs das motos que entraram na zona errada.
* **Log de Eventos:** Uma tabela com os últimos eventos registados pelo sistema.
* **Gráficos de Tendência:** Gráficos de pizza e barras que analisam as entradas por zona e a proporção de entradas corretas vs. incorretas.

---

## 4. Estrutura do Projeto

```bash
/
├── app/                      # Código principal da aplicação Flask
│   ├── static/               # Arquivos estáticos (CSS, JS)
│   │   ├── css/
│   │   │   └── styles.css    # Estilização do grid do pátio e dashboard
│   │   └── javascript/
│   │       └── script.js     # CÉREBRO DO FRONTEND: Unificado (JS + Gráficos),
│   │                         # consome as APIs e atualiza o HTML
│   ├── templates/
│   │   └── index.html        # Estrutura do dashboard e do grid do pátio
│   ├── __init__.py           # Inicialização da aplicação Flask (Factory)
│   ├── database.py           # Configuração do SQLAlchemy e modelo 'Telemetria'
│   ├── mqtt_client.py        # Cliente MQTT (O "Escritor" - Salva no Oracle)
│   └── routes.py             # Definição das APIs REST (O "Leitor" - Lê do Oracle)
├── circuit/                  # Arquivos do simulador Wokwi (ESP32)
├── .gitignore                # Ignora .env, venv/, __pycache__, etc.
├── .vscode/                  # Configurações do VSCode (opcional)
├── app.py                    # Script principal para iniciar a aplicação
├── init_db.py                # Script utilitário (para criar as tabelas no Oracle 1x)
├── readme.md                 # Esta documentação
└── requirements.txt          # Dependências do Python (Flask, SQLAlchemy, oracledb, ...)
```

## Como Executar o Projeto

### Pré-requisitos

- Python 3.10+
- [Node.js](https://nodejs.org/) 
- [Git](https://git-scm.com/)
- Editor de código (como o [VS Code](https://code.visualstudio.com/))
  
### 1. Clone o repositório
```bash
git clone https://github.com/30Lima/Iot_Heimdall.git
cd Iot_Heimdall
```
### 2. Crie o ambiente virtual (venv)
```bash
python -m venv venv
```

### 2. Entre no ambiente virtual (venv)
```bash
.\venv\Scripts\activate
```

### 3. Baixe as dependências
```bash
pip install -r requirements.txt
```

### 4. Acesse o sistema do ESP32 na plataforma wowki
```bash
https://wokwi.com/projects/442299333716121601
```

### 5. Execute o sistema do ESP32
<img width="1862" height="870" alt="image" src="https://github.com/user-attachments/assets/2acbe029-c058-4cea-b8b8-d7568cc816ed" />

### 6. No terminal do vscode (ou a sua IDE), execute
```bash
python app.py
```

### 7. Acesse o localhost (foi exibido no seu terminal) e veja o sistema funcionando
> Exemplo de localhost - http://127.0.0.1:5000

### Link do PITCH - IoT
```bash
https://youtu.be/QDE-c8H2k18
```

### Opcional - Caso queira rodar o banco na sua máquina, insira as credenciais em um .env e inicialize o script do banco
```bash
python init_db.py
```

---
© 2025 MontClio. Todos os direitos reservados.
