import os

from decouple import config

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model

os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY') # Resgatando chave API do .env



class BotVania:

    def __init__(self):
        self.__model = init_chat_model("gpt-4o-mini", model_provider="openai") # Inicia o modelo

    def invoke(self, question):
        prompt = PromptTemplate(
            input_variables=['texto'],
            template='''
            Você é a Vania Sales, uma especialista em vendas de AVCB/CLCB da Nakaya Engenharia. Sempre responda de forma amigável e simpática.
            Sempre responda com no maximo 250 caracteres.
            <texto>
            {texto}
            </texto>
            '''
        )                                               # Chain Simples: Cada componente “passa” seus resultados para o próximo automaticamente.
        chain = prompt | self.__model | StrOutputParser () # texto de entrada → prompt → modelo → parser → saída final.
        response = chain.invoke({                       
            'texto': question,
        })
        return response