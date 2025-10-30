import time
import random
from flask import Flask, request, jsonify
from bot.ai_bot import BotVania
from services.uazapi import Uazapi

app = Flask(__name__)

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json
    print(f"EVENTO RECEBIDO: {data}")

    # Verifica se é um evento de mensagem
    if data.get('EventType') != 'messages':
        return jsonify({'status': 'ignored', 'reason': 'não é mensagem'}), 200

    # Não há necessidade de tratar 'IsGroup' ou outros formatos recebidos no webhook, a API Uazapi já faz nativamente.
    # Verifica se é um evento 'fromMe'
    message_info = data.get('message', {}) # Pega o conteudo da msg

    # Ignora a mensagem. OBS: O 'if' faz somente valores 'true' acessarem o bloco.
    if message_info.get('fromMe', False):
        print("Mensagem FromME - Ignorando.")
        return jsonify({'status': 'ignored', 'reason': 'Mensagem FromMe'}), 200

    message_info = data.get('message', {})
    chat_id = message_info.get('chatid')
    text = message_info.get('text')

    if not chat_id or not text:
        return jsonify({'error': 'Dados de mensagem incompletos'}), 400

    uaz = Uazapi() # Instânciando classe
    ai_bot = BotVania()

    uaz.start_typing(number=chat_id) # Enviando presença de 'digitando...'

    time.sleep(random.randint(5, 10))

    response = ai_bot.invoke(question=text)

    uaz.send_message(
        number=chat_id, 
        message=response
        )

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
