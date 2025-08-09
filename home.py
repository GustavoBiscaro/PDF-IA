import streamlit as st
from langchain.memory import ConversationBufferMemory
from pathlib import Path
import time

PASTA_ARQUIVOS = Path(__file__).parent / 'files'

def cria_chain_conversa():
  st.session_state['chain'] = True

  memory = ConversationBufferMemory(return_messages=True)
  memory.chat_memory.add_user_message('Olá')
  memory.chat_memory.add_ai_message('Olá, eu sou o Chat IA Pro da Univesp!')
  st.session_state['memory'] = memory
  
  time.sleep(1)
  pass

def sidebar():
  uploaded_pdfs = st.file_uploader('Adicione somente arquivos em PDF', type=['.pdf'], accept_multiple_files=True
                   )
  if not uploaded_pdfs is None:
    for arquivo in PASTA_ARQUIVOS.glob('*.pdf'):
      arquivo.unlink()
    for pdf in uploaded_pdfs:
      with open(PASTA_ARQUIVOS / pdf.name, 'wb') as f:
        f.write(pdf.read())

  label_botao = 'Inicializar Chatbot'
  if 'chain' in st.session_state:
    label_botao = 'Atualizar o Chat'

  if st.button(label_botao, use_container_width=True):
    if len(list(PASTA_ARQUIVOS.glob('*.pdf'))) == 0:
      st.error('Adicione arquivos .pdf para iniciar o Chatbot')
    else:
      st.success('Inicializando o Chatbot...')
      cria_chain_conversa()
      st.rerun()
      
def chat_window():
  st.header('🤖 Bem-vindo ao Chat IA Pro da Univesp', divider=True)

  if not 'chain' in st.session_state:
    st.error('Faça o upload de PDFs para iniciar!')
    st.stop()

  # chain = st.session_state['chain']
  # memory = chain.memory

  memory = st.session_state['memory']
  messages = memory.load_memory_variables({})['history']

  container = st.container()
  for message in messages:
    chat = container.chat_message(message.type)
    chat.markdown(message.content)

  new_message = st.chat_input('Inicie uma nova conversa...')
  if new_message:
    chat = container.chat_message('human')
    chat.markdown(new_message)
    chat = container.chat_message('ai')
    chat.markdown('Gerando sua resposta')

    time.sleep(2)
    memory.chat_memory.add_user_message(new_message)
    memory.chat_memory.add_ai_message('Olá, eu sou o Chat IA Pro da Univesp! O que gostaria de saber?')
    st.rerun()

    
    
  
  

    


def main():
  with st.sidebar:
    sidebar()
  chat_window()

if __name__ == '__main__':
  main()