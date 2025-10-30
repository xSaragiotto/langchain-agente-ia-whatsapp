import requests


class Uazapi:
    def __init__(self):
        self.__api_url = 'https://freeuazapigo.uazapi.com'
        self.__token = '4429424e-2aa3-4a0b-88f4-d9b37def1aa9'
        
    def clean_number(self, number: str) -> str: # Removemos o sufixo '@s.whatsapp.net' se existir
        return number.replace('@s.whatsapp.net', '').strip()

    def send_message(self, number, message): # Envia uma mensagem de texto via UazAPI.

        clean_number = self.clean_number(number) 

        url = f'{self.__api_url}/send/text'
        headers = {
            "Accept": "application/json",
            "token": self.__token,
            "Content-Type": "application/json"
        }
        payload = {
            "number": clean_number,
            "text": message,
        }

        print(f"📤 Enviando mensagem para {clean_number}: {message}") # Console log

        response = requests.post(url, json=payload, headers=headers)

        print(f"🔁 Status: {response.status_code}, resposta: {response.text}") # Console log
        return response

    def start_typing(self, number): # Envia presença 'digitando...' via UazAPI.
        
        clean_number = self.clean_number(number)

        url = f'{self.__api_url}/message/presence'
        headers = {
            "Accept": "application/json",
            "token": self.__token,
            "Content-Type": "application/json"
        }
        payload = {
            "number": clean_number,
            "presence": "composing",
            "delay": 30000,
        }

        print(f"Enviando presença de 'digitando...' para: {clean_number}") # Console Log

        response = requests.post(url, json=payload, headers=headers)

        print(f"Status: {response.status_code}, resposta: {response.text}") # Console Log
        return response