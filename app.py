import streamlit as st
from openai import OpenAI

st.title("Mon Application IA")
st.write("Bienvenue mon frère ! Ceci est la base de notre projet.")

# Configuration des clients IA
def get_groq_client():
    return OpenAI(
        api_key=st.secrets["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1"
    )

def get_openrouter_client():
    return OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )

# Initialiser l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher les messages existants
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Pose ta question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("L'IA réfléchit..."):
            try:
                # Essayer Groq en premier (ultra rapide)
                client = get_groq_client()
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                )
                reponse_ia = response.choices[0].message.content
            except Exception as e:
                # Si Groq plante, on bascule sur OpenRouter
                st.warning("Groq est indisponible, basculement sur OpenRouter...")
                try:
                    client = get_openrouter_client()
                    response = client.chat.completions.create(
                        model="meta-llama/llama-3.3-70b-instruct",
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                    )
                    reponse_ia = response.choices[0].message.content
                except Exception as e2:
                    reponse_ia = f"Désolé mon frère, les deux serveurs sont saturés. Erreur : {str(e2)}"
            
            st.markdown(reponse_ia)
            st.session_state.messages.append({"role": "assistant", "content": reponse_ia})
