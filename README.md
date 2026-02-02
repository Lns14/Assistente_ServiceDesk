# Abertura de demandas via voz para o Jira

Projeto simples para abrir chamados no Jira a partir da fala do usuário.

O sistema grava a voz, transcreve o áudio, organiza o texto com IA e cria automaticamente um chamado no Jira.

---

## Como funciona

1. O sistema pede o problema por áudio  
2. O usuário grava a resposta  
3. O áudio é transcrito com Whisper  
4. O texto é organizado pelo ChatGPT  
5. Um chamado é criado no Jira  
6. A confirmação é falada para o usuário  

---

## Requisitos

- Executar no Google Colab
- Microfone habilitado

Bibliotecas usadas:

- gTTS  
- whisper  
- openai  
- requests  

---

## Variáveis no Colab

Configurar no `userdata`:

- OPENAI_API_KEY  
- JIRA_EMAIL  
- JIRA_API_TOKEN  
- JIRA_DOMAIN  

---

## Objetivo

Automatizar a abertura de chamados no Jira a partir de áudio.
