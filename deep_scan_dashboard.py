import streamlit as st
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

# Set page config
st.set_page_config(page_title="DeepScan", page_icon="🔍", layout="wide")

# Theme toggle
theme = st.sidebar.selectbox("🌓 Theme", ["Light", "Dark"])
primary_color = "#0a0a0a" if theme == "Dark" else "#0066cc"
bg_color = "#1e1e1e" if theme == "Dark" else "#ffffff"
text_color = "#ffffff" if theme == "Dark" else "#000000"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .sidebar .sidebar-content {{
        background-color: {bg_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Session state for stats
if 'total_scans' not in st.session_state:
    st.session_state.total_scans = 0
    st.session_state.risky_scans = 0
    st.session_state.last_email = ""

# --- Sidebar ---
st.sidebar.title("🔍 DeepScan")
st.sidebar.markdown("AI-Powered Dark Web Scanner")
st.sidebar.markdown("---")
st.sidebar.markdown("👤 **Total Scans:** " + str(st.session_state.total_scans))
st.sidebar.markdown("⚠️ **Risky Scans:** " + str(st.session_state.risky_scans))
if st.session_state.total_scans > 0:
    risky_percent = round((st.session_state.risky_scans / st.session_state.total_scans) * 100, 1)
    st.sidebar.markdown(f"📊 **Risk %:** {risky_percent}%")
else:
    st.sidebar.markdown("📊 **Risk %:** 0%")

if st.session_state.last_email:
    st.sidebar.markdown(f"📬 **Last Scanned:** `{st.session_state.last_email}`")

st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ by Aditya")

# --- Leak Functions ---
def load_fake_darkweb_page():
    with open("test_darkweb_page.html", "r", encoding="utf-8") as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    return html, soup.get_text()

def check_email_leak(user_email, text):
    leaked_items = []

    if user_email in text:
        leaked_items.append(("Email", user_email))

    passwords = re.findall(r"[Pp]assword[:\s]+(\S+)", text)
    if passwords:
        leaked_items.append(("Password", passwords[0]))

    cards = re.findall(r"\b(?:\d[ -]*?){13,16}\b", text)
    if cards:
        leaked_items.append(("Credit Card", cards[0]))

    return leaked_items

# --- Main UI ---
st.title("🛡️ DeepScan – Dark Web Email Leak Checker")
st.markdown("Enter your email to scan a simulated dark web database for potential leaks.")

email = st.text_input("📨 Enter your email")

if st.button("🔎 Scan Now"):
    if email:
        # Simulate scan loading
        with st.spinner("🧠 Scanning dark web sources using AI..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.03)
                progress.progress(i + 1)

        html_code, page_text = load_fake_darkweb_page()
        results = check_email_leak(email, page_text)

        st.session_state.total_scans += 1
        st.session_state.last_email = email
        st.caption("🔗 Source: http://darkleaksxyzabc.onion/forum/leaks/2025")
        st.expander("🧾 View Dark Web Page").code(html_code, language='html')

        if results:
            st.session_state.risky_scans += 1
            st.error("🚨 Leak Found!")
            df = pd.DataFrame(results, columns=["Leak Type", "Value"])
            st.table(df)

            # ✅ Report Button
            if st.button("🚨 Report This Leak"):
                with st.spinner("Sending report to security team..."):
                    time.sleep(2)
                st.success("✅ Leak reported. Our team will investigate.")

            risk_score = sum(
                30 if kind == "Email" else
                40 if kind == "Password" else
                50 if kind == "Credit Card" else 0
                for kind, _ in results
            )

            if risk_score >= 80:
                risk_level = "🟥 HIGH"
            elif risk_score >= 40:
                risk_level = "🟧 MEDIUM"
            else:
                risk_level = "🟩 LOW"

            st.markdown(f"**🛑 Risk Score:** `{risk_score}` — {risk_level}")
        else:
            st.success("✅ No leak found. You're safe!")

        if st.button("🔄 Scan Another"):
            st.experimental_rerun()
    else:
        st.warning("⚠️ Please enter a valid email.")
