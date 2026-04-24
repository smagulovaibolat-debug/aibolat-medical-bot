services:
  - type: worker
    name: aibolat-medical-bot-v2
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: TELEGRAM_TOKEN
        sync: false
      - key: GEMINI_KEY
        sync: false
