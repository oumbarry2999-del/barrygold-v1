import streamlit as st
import MetaTrader5 as mt5
from auth import show_login
from datetime import datetime

st.set_page_config(
    page_title="BarryGold",
    page_icon="🥇",
    layout="wide"
)

# Vérifier si connecté
if "user" not in st.session_state:
    show_login()
    st.stop()

user = st.session_state.user

# SIDEBAR
with st.sidebar:
    st.markdown(f"### 👤 {user['prenom']} {user['nom']}")
    st.markdown(f"📧 {user['email']}")
    st.divider()
    page = st.radio("Navigation", [
        "📊 Dashboard",
        "🔗 Connecter MT5",
        "🤖 Robot",
        "📈 Historique",
        "⚙️ Paramètres"
    ])
    st.divider()
    if st.button("🚪 Déconnexion"):
        del st.session_state.user
        st.rerun()

# DASHBOARD
if page == "📊 Dashboard":
    st.title(f"Bonjour {user['prenom']} 👋")

    if mt5.initialize():
        info = mt5.account_info()
        tick = mt5.symbol_info_tick("XAUUSD")
        nb_trades = mt5.history_deals_total(
            0, int(datetime.now().timestamp())
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Solde", f"${info.balance:,.2f}")
        col2.metric("📈 Équité", f"${info.equity:,.2f}")
        col3.metric("🥇 XAUUSD", f"{tick.bid:,.2f}")
        col4.metric("🔢 Trades", nb_trades)

        # Profits/Pertes
        profit = info.equity - info.balance
        st.divider()
        col5, col6 = st.columns(2)
        col5.metric("📊 Profit/Perte", f"${profit:,.2f}",
                    delta=f"{profit:,.2f}")
        col6.metric("🏦 Marge libre", f"${info.margin_free:,.2f}")

        mt5.shutdown()
    else:
        st.warning("⚠️ MT5 non connecté — allez dans 'Connecter MT5'")

# CONNEXION MT5
elif page == "🔗 Connecter MT5":
    st.title("🔗 Connecter votre compte MT5")

    broker = st.selectbox("Broker", [
        "MetaQuotes-Demo",
        "Exness-MT5",
        "XMTrading-MT5",
        "ICMarketsSC-MT5"
    ])
    login = st.number_input("Numéro de compte", min_value=0)
    password = st.text_input("Mot de passe", type="password")

    if st.button("🔗 Connecter", use_container_width=True):
        if mt5.initialize(login=int(login),
                         password=password,
                         server=broker):
            st.success("✅ Connecté à MT5 !")
            st.session_state.mt5_login = login
            st.session_state.mt5_password = password
            st.session_state.mt5_server = broker
        else:
            st.error("❌ Connexion échouée")

# ROBOT
elif page == "🤖 Robot":
    st.title("🤖 Robot XAUUSD")

    col1, col2 = st.columns(2)
    with col1:
        lot = st.number_input("Lot Size", value=1.0)
        sl = st.number_input("Stop Loss (pts)", value=100)
        be = st.number_input("Break Even (pts)", value=100)
    with col2:
        tp = st.number_input("Take Profit (pts)", value=1000)
        close_hour = st.number_input("Heure fermeture", value=22)
        distance = st.number_input("Distance Breakout (pts)", value=50)

    st.divider()
    if st.button("▶️ Démarrer Robot", use_container_width=True):
        st.session_state.robot_on = True
        st.success("✅ Robot démarré !")
    if st.button("⏹️ Arrêter Robot", use_container_width=True):
        st.session_state.robot_on = False
        st.error("⏹️ Robot arrêté !")

    status = "🟢 Actif" if st.session_state.get("robot_on") else "🔴 Inactif"
    st.metric("Statut", status)

# HISTORIQUE
elif page == "📈 Historique":
    st.title("📈 Historique des trades")

    if mt5.initialize():
        deals = mt5.history_deals_get(0, int(datetime.now().timestamp()))
        if deals:
            import pandas as pd
            df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df = df[['time', 'symbol', 'type', 'volume', 'price', 'profit']]
            st.dataframe(df, use_container_width=True)
            st.metric("💰 Profit total", f"${df['profit'].sum():,.2f}")
        else:
            st.info("Aucun trade dans l'historique")
        mt5.shutdown()
    else:
        st.warning("⚠️ Connectez MT5 d'abord")

# PARAMÈTRES
elif page == "⚙️ Paramètres":
    st.title("⚙️ Paramètres")
    prenom = st.text_input("Prénom", value=user['prenom'])
    nom = st.text_input("Nom", value=user['nom'])
    email = st.text_input("Email", value=user['email'])
    if st.button("💾 Sauvegarder", use_container_width=True):
        st.success("✅ Sauvegardé !")
