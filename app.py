import streamlit as st
import google.generativeai as genai

# Configuração da Página
st.set_page_config(page_title="Ordem dos Investigadores: Vitanova", page_icon="🕵️‍♂️")

# Estilo Vitanova (Dark Mode Pedagógico)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stChatInput { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🕵️‍♂️ Terminal da Ordem: Vitanova")
st.caption("Conexão Segura com o Mestre Investigador - 5ºD")

# Pegar a Chave da API (Vamos configurar isso no próximo passo)
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# Configuração do Modelo (Fiel ao que você testou)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # Ou o 2.0 se preferir
    system_instruction="VOCÊ É O MESTRE INVESTIGADOR... (Cole aqui todas as instruções que criamos antes)"
)

# Histórico de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do Aluno
if prompt := st.chat_input("Relate sua descoberta ou dúvida..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta da IA
    with st.chat_message("assistant"):
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]
        ])
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
