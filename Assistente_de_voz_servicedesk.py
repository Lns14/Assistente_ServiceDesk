# -*- coding: utf-8 -*-
language = 'pt'

"""# 1. Executando primeiro contato com usuário"""

from gtts import  gTTS
from IPython.display import Audio, display

# Cria um objeto gTTS com a resposta gerada pelo ChatGPT e a língua que será sintetizada em voz (variável "language").
gtts_object = gTTS(text="Olá! Explique em poucas palavras e de forma clara o seu problema para que possamos te ajudar.", lang=language, slow=False)

# Salva o áudio da resposta no arquivo especificado (pasta padrão do Google Colab)
response_audio = "/content/response_audio.wav"
gtts_object.save(response_audio)

# Reproduz o áudio da resposta salvo no arquivo
display(Audio(response_audio, autoplay=True))

"""# 2. Gravação de Áudio Com Python sobre a necessidade do usuário"""

from IPython.display import Audio, display, Javascript
from google.colab import output
from base64 import b64decode

# Código JavaScript para gravar áudio do usuário usando a "MediaStream Recording API"
RECORD = """
const sleep  = time => new Promise(resolve => setTimeout(resolve, time))
const b2text = blob => new Promise(resolve => {
  const reader = new FileReader()
  reader.onloadend = e => resolve(e.srcElement.result)
  reader.readAsDataURL(blob)
})
var record = time => new Promise(async resolve => {
  stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  recorder = new MediaRecorder(stream)
  chunks = []
  recorder.ondataavailable = e => chunks.push(e.data)
  recorder.start()
  await sleep(time)
  recorder.onstop = async ()=>{
    blob = new Blob(chunks)
    text = await b2text(blob)
    resolve(text)
  }
  recorder.stop()
})
"""

def record(sec=5):
  # Executa o código JavaScript para gravar o áudio
  display(Javascript(RECORD))
  # Recebe o áudio gravado como resultado do JavaScript
  js_result = output.eval_js('record(%s)' % (sec * 1000))
   # Decodifica o áudio em base64
  audio = b64decode(js_result.split(',')[1])
  # Salva o áudio em um arquivo
  file_name = 'request_audio.wav'
  with open(file_name, 'wb') as f:
    f.write(audio)
  # Retorna o caminho do arquivo de áudio (pasta padrão do Google Colab)
  return f'/content/{file_name}'

# Grava o áudio do usuário por um tempo determinado (padrão 5 segundos)
print('Ouvindo...\n')
record_file = record()

# Exibe o áudio gravado
display(Audio(record_file, autoplay=False))

"""# 2. Reconhecimento de Fala com Whisper (OpenAI)"""
import whisper
model = whisper.load_model("small")

# Transcreve o audio gravado anteriormente.
result = model.transcribe(record_file, fp16=False, language=language)
transcription = result["text"]
print(transcription)

"""# 3. Interpretação da fala pelo ChatGPT"""

import openai
import os
from google.colab import userdata
userdata.get('OPENAI_API_KEY')

# Prompt para o ChatGPT
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": (
                "Você é um analista de Service Desk. "
                "Sua tarefa é transformar reclamações faladas em chamados técnicos bem estruturados. "
                "Crie um título curto e uma descrição clara e profissional. "
                "Não invente informações e não use linguagem informal."
            )
        },
        {
            "role": "user",
            "content": (
                f"A partir do texto abaixo, gere:\n"
                f"1. Um título curto (summary) com no máximo 10 palavras\n"
                f"2. Uma descrição profissional\n\n"
                f"Texto do usuário:\n\"{transcription}\"\n\n"
                f"Responda APENAS em JSON no formato:\n"
                f"{{\n"
                f'  "summary": "...",\n'
                f'  "description": "..."\n'
                f"}}"
            )
        }
    ],
    temperature=0.2
)

# Resposta do modelo
chatgpt_response = response.choices[0].message.content
print(chatgpt_response)

"""# 4. Abertura de chamado com a necessidade do usuário"""

import requests
from requests.auth import HTTPBasicAuth
import json
from google.colab import userdata
userdata.get('JIRA_EMAIL')
from google.colab import userdata
userdata.get('JIRA_API_TOKEN')
from google.colab import userdata
userdata.get('JIRA_DOMAIN')

# Endpoint
url = f"https://{JIRA_DOMAIN}/rest/api/3/issue"

# Autenticação
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

# Headers
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Payload do chamado
payload = {
    "fields": {
        "project": {
            "key": "DESK"
        },
        "summary": chatgpt_response.summary,
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": chatgpt_response.description
                        }
                    ]
                }
            ]
        },
        "issuetype": {
            "name": "[System] Incident"
        },
        "priority": {
            "name": "High"
        },
        "labels": ["voz", "windows", "notebook"]
    }
}

# Requisição
response = requests.post(
    url,
    headers=headers,
    auth=auth,
    data=json.dumps(payload)
)

# Resultado
if response.status_code == 201:
    issue_key = response.json()["key"]
    resultado = f"Chamado criado com sucesso: {issue_key}. Você receberá atualizações sobre sua demanda via e-mail. Obrigado!"
    print(resultado)
else:
    print("Erro ao criar chamado")
    print(response.status_code)
    print(response.text)

"""# 4. Sintetizando a Resposta para o usuário (gTTS)"""

from gtts import  gTTS

# Cria um objeto gTTS com a resposta gerada pelo ChatGPT e a língua que será sintetizada em voz (variável "language").
gtts_object = gTTS(text=resultado, lang=language, slow=False)

# Salva o áudio da resposta no arquivo especificado (pasta padrão do Google Colab)
response_audio = "/content/response_audio.wav"
gtts_object.save(response_audio)

# Reproduz o áudio da resposta salvo no arquivo
display(Audio(response_audio, autoplay=True))