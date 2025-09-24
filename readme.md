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

```