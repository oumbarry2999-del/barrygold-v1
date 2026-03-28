import streamlit as st
from database import create_user, login_user

def show_login():
    st.markdown("""
    <style>
    .login-box { max-width: 400px; margin: auto; }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🥇 BarryGold")
    st.subheader("Robot de Trading XAUUSD")
    
    tab1, tab2 = st.tabs(["Se connecter", "S'inscrire"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Mot de passe", type="password", key="login_pass")
        
        if st.button("Se connecter", use_container_width=True):
            user = login_user(email, password)
            if user:
                st.session_state.user = {
                    "id": user[0],
                    "prenom": user[1],
                    "nom": user[2],
                    "email": user[3]
                }
                st.success("Connecté !")
                st.rerun()
            else:
                st.error("Email ou mot de passe incorrect")
    
    with tab2:
        prenom = st.text_input("Prénom")
        nom = st.text_input("Nom")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Mot de passe", type="password", key="reg_pass")
        
        if st.button("Créer mon compte", use_container_width=True):
            if create_user(prenom, nom, email, password):
                st.success("Compte créé ! Connectez-vous.")
            else:
                st.error("Email déjà utilisé !")
