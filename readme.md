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
│   ├── __pycache__/               # Cache do Python (não versionar)
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
├── app.py                         # Script principal para iniciar a aplicação Flask
├── readme.md                      # Documentação e descrição do projeto
├── requirements.txt               # Dependências do projeto
```

