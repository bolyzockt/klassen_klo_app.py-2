import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- CONFIG ---
st.set_page_config(page_title="Herr Dietschs krasses Terminal - 9g", page_icon="🚀", layout="wide")

@st.cache_resource
def get_permanent_log():
    return {"df": pd.DataFrame(columns=["Datum", "Name", "Von", "Bis", "Dauer"])}

db = get_permanent_log()

if 'auf_klo' not in st.session_state:
    st.session_state.auf_klo = {}

# DEINE KLASSE 9g
SCHUELER_INFO = {
    "Ahmad": "⚡", "Rean": "🔥", "Zeynep": "🌸", "Nicolo": "🧊", 
    "Hamza": "🐹", "Bilind": "🌋", "Luka": "🌊", "Marios": "💎", 
    "Kaja": "🦦", "Gencho": "🚀", "Stjepan": "🍀", "Leandro": "👑",
    "Zuzanna": "🌈", "Matija": "🌙", "Zoltan": "🔮", "Dominik": "✨"
}

GEHEIMES_PW = "LeonKing"
ALARM_MINUTEN = 15

wer_ist_weg = list(st.session_state.auf_klo.keys())[0] if st.session_state.auf_klo else None

ist_alarm = False
sekunden_weg = 0
if wer_ist_weg:
    sekunden_weg = int((datetime.now() - st.session_state.auf_klo[wer_ist_weg]).total_seconds())
    if sekunden_weg >= ALARM_MINUTEN * 60:
        ist_alarm = True

bg_color = "#FF0000" if ist_alarm else ("#8A2BE2" if wer_ist_weg else "#1e1233")

# --- STYLE OPTIMIERT FÜR EMOJIS + RIESEN TEXT ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; transition: background 0.5s ease; color: white; }}
    .ultra-title {{ text-align: center; font-size: 40px !important; font-weight: 900; margin-bottom: 20px; }}
    
    /* BUTTON STYLING */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px !important;
        height: 140px !important; 
        width: 100% !important;
    }}

    /* TEXT & EMOJI GRÖSSE */
    div.stButton > button div[data-testid="stMarkdownContainer"] p {{
        font-size: 40px !important; 
        font-weight: 900 !important;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        color: white !important;
    }}
    
    /* Besetzter Status (Weißer Button) */
    div[data-testid="stButton"] button:has(p:contains("🚽")) {{
        background-color: white !important;
    }}
    div[data-testid="stButton"] button:has(p:contains("🚽")) p {{
        color: black !important;
    }}

    .alarm-text {{ color: yellow; font-weight: bold; text-align: center; font-size: 35px; animation: blink 1s infinite; }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}
    header {{visibility: hidden;}} footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="ultra-title">🚀 HERR DIETSCH’S KRASSES TERMINAL 9g 🚀</div>', unsafe_allow_html=True)

# DASHBOARD
c1, c2, c3 = st.columns(3)
with c1: st.metric("👥 IM RAUM", f"{len(SCHUELER_INFO) - (1 if wer_ist_weg else 0)}")
with c2: st.metric("🚽 STATUS", "BESETZT 🛑" if wer_ist_weg else "FREI ✅")
if wer_ist_weg:
    m, s = divmod(sekunden_weg, 60)
    with c3: st.metric("⏳ ZEIT WEG", f"{m:02d}:{s:02d}")
    if ist_alarm:
        st.markdown(f'<div class="alarm-text">⚠️ ALARM: {wer_ist_weg} ÜBERFÄLLIG! ⚠️</div>', unsafe_allow_html=True)

st.write("---")

# GRID
cols = st.columns(3)
namen_sortiert = sorted(SCHUELER_INFO.keys())
for i, name in enumerate(namen_sortiert):
    with cols[i % 3]:
        ist_dieser_weg = (wer_ist_weg == name)
        emoji = SCHUELER_INFO[name]
        label = f"🚽 {name}" if ist_dieser_weg else f"{emoji} {name}"
        
        if st.button(label, key=f"btn_{name}", use_container_width=True, disabled=(wer_ist_weg is not None and not ist_dieser_weg)):
            jetzt = datetime.now()
            if not ist_dieser_weg:
                st.session_state.auf_klo[name] = jetzt
                st.rerun()
            else:
                start_zeit = st.session_state.auf_klo.pop(name)
                diff = jetzt - start_zeit
                m, s = divmod(int(diff.total_seconds()), 60)
                db["df"] = pd.concat([db["df"], pd.DataFrame([{"Datum": jetzt.strftime("%d.%m.%Y"), "Name": name, "Von": start_zeit.strftime("%H:%M:%S"), "Bis": jetzt.strftime("%H:%M:%S"), "Dauer": f"{m}m {s}s"}])], ignore_index=True)
                st.rerun()

# ADMIN
with st.expander("🛠️ ADMIN"):
    if st.text_input("Code", type="password") == GEHEIMES_PW:
        st.dataframe(db["df"], use_container_width=True)
        if st.button("🗑️ CLEAR"):
            db["df"] = pd.DataFrame(columns=["Datum", "Name", "Von", "Bis", "Dauer"])
            st.rerun()
        st.write("© 2026 bolyzockt")

if wer_ist_weg:
    time.sleep(2)
    st.rerun()


