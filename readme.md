# HEIMDALL - Localização e Monitoramento de Motos no Pátio
> Solução para o challenge da Mottu promovido pela FIAP

## Integrantes

| Nome Completo               | RM       |
|-----------------------------|----------|
| Pedro Henrique Lima Santos  | 558243   |
| Vitor Gomes Martins         | 558244   |
| Leonardo Pimentel Santos    | 557541   |

## Descrição da Solução

O **HEIMDALL** é uma solução integrada composta por um aplicativo mobile (React Native) e um sistema de simulação com IoT e dashboard web (Python + Flask + MQTT). Seu objetivo é facilitar o processo de **localização e monitoramento de motocicletas dentro do pátio logístico da Mottu**, organizando as motos por zonas e exibindo logs de entrada em tempo real.

### Funcionalidades

- **Aplicativo mobile** com navegação via Drawer, telas de Splash, Login, Cadastro, Home, Perfil e Sobre.
- Armazenamento local do nome de usuário com `AsyncStorage`.
- Interface desenvolvida com foco em acessibilidade, responsividade e boas práticas de UX.
- **Dashboard web** que exibe em tempo real os logs das entradas das motos no pátio com nome da zona, placa e horário.
- Integração MQTT para simular envio automático de dados de sensores IoT.

---

## Estrutura do Projeto

```bash
/
├── app/                           # Código principal da aplicação Flask
│   ├── static/                    # Arquivos estáticos do sistema
│   │   ├── css/                   # Arquivos de estilo
│   │   │   └── styles.css         # Estilização da interface do dashboard
│   │   ├── javascript/            # Scripts JavaScript
│   │   │   ├── graph.js           # Lógica de exibição e atualização dos gráficos
│   │   │   └── script.js          # Funções para exibir e atualizar logs em tempo real
│   ├── templates/                 # Arquivos HTML
│   │   └── index.html             # Estrutura da interface do dashboard
│   ├── __init__.py                # Inicialização da aplicação Flask
│   ├── mqtt_client.py             # Cliente MQTT para comunicação com o Wokwi/ESP32
│   ├── routes.py                  # Definição das rotas da aplicação
├── circuit/                       # Arquivos relacionados ao circuito ESP32
│   ├── code/                      # Código-fonte do ESP32
│   ├── images/                    # Imagens do circuito
│   ├── diagram.json               # Diagrama do circuito (Wokwi)
│   └── libraries.txt              # Bibliotecas necessárias para executar o circuito
├── data/                          # Armazenamento de dados
│   └── data.json                  # Logs recebidos do ESP32
├── system_images/                 # Imagens usadas no sistema/dashboard
├── .gitignore                     # Define arquivos e pastas que não serão versionados pelo Git
├── app.py                         # Script principal para iniciar a aplicação Flask
├── readme.md                      # Documentação e descrição do projeto
├── requirements.txt               # Dependências do projeto
```

### 🌐 Configuração do Broker MQTT

Broker:        HiveMQ (broker público)
Endereço:      broker.hivemq.com
Porta:         1883
Tópico:        esp32/dados
Protocolo:     MQTT v3.1.1

---

### 🗂 Arquivo gerado

Caminho:    data/data.json  
Formato:    JSON  
Conteúdo:   Array de objetos contendo os dados do ESP32 com timestamps  

> 💡 Este fluxo permite armazenar com segurança e em tempo real os dados recebidos do ESP32, garantindo que possam ser utilizados posteriormente pela API Flask e exibidos na interface web.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- [Node.js](https://nodejs.org/) 
- [Git](https://git-scm.com/)
- Editor de código (como o [VS Code](https://code.visualstudio.com/))

### 1. Clone o repositório
```bash
git clone https://github.com/30Lima/Iot_Heimdall.git
cd Iot_Heimdall
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Acesse o sistema do ESP32 na plataforma wowki
```bash
https://wokwi.com/projects/442299333716121601
```

### 4. Execute o sistema do ESP32
<img width="1862" height="870" alt="image" src="https://github.com/user-attachments/assets/2acbe029-c058-4cea-b8b8-d7568cc816ed" />

### 5. No terminal do vscode (ou a sua IDE), execute
```bash
python app.py
```

### 6. Acesse o localhost (foi exibido no seu terminal) e veja o sistema funcionando
> Exemplo de localhost - http://127.0.0.1:5000

### Link do PITCH - IoT
```bash
https://youtu.be/QDE-c8H2k18
```

---
© 2025 MontClio. Todos os direitos reservados.
