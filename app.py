import streamlit as st

st.title("Mon Application IA")
st.write("Bienvenue mon frère ! Ceci est la base de notre projet.")

# Initialiser l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher les messages existants
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Pose ta question..."):
    # Afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse simulée (on la remplacera par l'IA plus tard)
    response = "Ceci est une réponse simulée. L'IA sera connectée à l'étape suivante."
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
