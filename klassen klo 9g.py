import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- CONFIG ---
st.set_page_config(page_title="Herr Dietsch’s krasses Terminal - 9g", page_icon="🚀", layout="wide")

# --- GLOBALER SPEICHER ---
@st.cache_resource
def get_permanent_log():
    return {"df": pd.DataFrame(columns=["Datum", "Name", "Von", "Bis", "Dauer"])}

db = get_permanent_log()

if 'auf_klo' not in st.session_state:
    st.session_state.auf_klo = {}

# DEINE KLASSE 9g (2026 Edition)
SCHUELER_INFO = {
    "Ahmad": {"emoji": "⚡"}, "Rean": {"emoji": "🔥"}, "Zeynep": {"emoji": "🌸"},
    "Nicolo": {"emoji": "🧊"}, "Hamza": {"emoji": "🐹"}, "Bilind": {"emoji": "🌋"},
    "Luka": {"emoji": "🌊"}, "Marios": {"emoji": "💎"}, "Kaja": {"emoji": "🦦"},
    "Gencho": {"emoji": "🚀"}, "Stjepan": {"emoji": "🍀"}, "Leandro": {"emoji": "👑"},
    "Zuzanna": {"emoji": "🌈"}, "Matija": {"emoji": "🌙"}, "Zoltan": {"emoji": "🔮"},
    "Dominik": {"emoji": "✨"}
}

# PASSWORT & SETTINGS
GEHEIMES_PW = "LeonKing"
ALARM_MINUTEN = 15

# Wer ist weg?
wer_ist_weg = list(st.session_state.auf_klo.keys())[0] if st.session_state.auf_klo else None

# Alarm-Logik
ist_alarm = False
sekunden_weg = 0
if wer_ist_weg:
    sekunden_weg = int((datetime.now() - st.session_state.auf_klo[wer_ist_weg]).total_seconds())
    if sekunden_weg >= ALARM_MINUTEN * 60:
        ist_alarm = True

# Hintergrundfarbe
bg_color = "#FF0000" if ist_alarm else ("#8A2BE2" if wer_ist_weg else "#1e1233")

# --- STYLE ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; transition: background 0.5s ease; color: white; }}
    .ultra-title {{ text-align: center; font-size: 50px !important; font-weight: 900; text-shadow: 0 0 20px white; margin-bottom: 20px; }}
    
    /* EXTREM GROSSE NAMEN */
    .stButton>button {{
        background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
        border: 3px solid rgba(255, 255, 255, 0.3); border-radius: 20px;
        color: white; 
        height: 150px !important;    /* Buttons noch höher */
        font-size: 45px !important;  /* SCHRIFT EXTREM GROSS */
        font-weight: 900 !important;
        text-transform: uppercase;
        margin-bottom: 10px;
    }}
    
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}
    .alarm-text {{ color: yellow; font-weight: bold; text-align: center; font-size: 35px; animation: blink 1s infinite; border: 3px dashed yellow; border-radius: 10px; padding: 10px; }}
    div[data-testid="stButton"] button:contains("🚽") {{ background: white !important; color: black !important; border: 6px solid gold !important; }}
    .copyright {{ text-align: center; font-size: 14px; color: rgba(255,255,255,0.3); margin-top: 50px; }}
    header {{visibility: hidden;}} footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="ultra-title">🚀 HERR DIETSCH’S KRASSES TERMINAL 9g 🚀</div>', unsafe_allow_html=True)

# --- DASHBOARD ---
c1, c2, c3 = st.columns(3)
with c1: st.metric("👥 IM RAUM", f"{len(SCHUELER_INFO) - (1 if wer_ist_weg else 0)}")
with c2: st.metric("🚽 STATUS", "BESETZT 🛑" if wer_ist_weg else "FREI ✅")
if wer_ist_weg:
    m, s = divmod(sekunden_weg, 60)
    with c3: st.metric("⏳ ZEIT WEG", f"{m:02d}:{s:02d}")
    if ist_alarm:
        st.markdown(f'<div class="alarm-text">⚠️ ALARM: {wer_ist_weg} ÜBERFÄLLIG! ⚠️</div>', unsafe_allow_html=True)

st.write("---")

# --- GRID (1 Spalte für maximale Schriftbreite) ---
namen_sortiert = sorted(SCHUELER_INFO.keys())
for name in namen_sortiert:
    ist_dieser_weg = (wer_ist_weg == name)
    info = SCHUELER_INFO[name]
    label = f"🚽 {info['emoji']} {name}" if ist_dieser_weg else f"{info['emoji']} {name}"
    
    if st.button(label, key=f"btn_{name}", use_container_width=True, disabled=(wer_ist_weg is not None and not ist_dieser_weg)):
        jetzt = datetime.now()
        if not ist_dieser_weg:
            st.session_state.auf_klo[name] = jetzt
            st.rerun()
        else:
            start_zeit = st.session_state.auf_klo.pop(name)
            diff = jetzt - start_zeit
            m, s = divmod(int(diff.total_seconds()), 60)
            neue_daten = pd.DataFrame([{"Datum": jetzt.strftime("%d.%m.%Y"), "Name": name, "Von": start_zeit.strftime("%H:%M:%S"), "Bis": jetzt.strftime("%H:%M:%S"), "Dauer": f"{m}m {s}s"}])
            db["df"] = pd.concat([db["df"], neue_daten], ignore_index=True)
            st.rerun()

# --- ADMIN TERMINAL ---
st.write("---")
with st.expander("🛠️ ADMIN TERMINAL"):
    pw_input = st.text_input("Identity Verification", type="password", placeholder="Access Code...")
    if pw_input == GEHEIMES_PW:
        st.success("Access Granted.")
        st.dataframe(db["df"], use_container_width=True)
        csv = db["df"].to_csv(index=False).encode('utf-8')
        st.download_button(label="💾 DOWNLOAD LOGS", data=csv, file_name="Dietsch_Log_9g_2026.csv", mime="text/csv")
        if st.button("🗑️ CLEAR MEMORY"):
            db["df"] = pd.DataFrame(columns=["Datum", "Name", "Von", "Bis", "Dauer"])
            st.rerun()
        st.write("© 2026 bolyzockt")
    elif pw_input != "":
        st.error("Invalid Code.")

st.markdown('<div class="copyright">© 2026 bolyzockt - Herr Dietsch’s krasses Terminal 9g</div>', unsafe_allow_html=True)

if wer_ist_weg:
    time.sleep(2)
    st.rerun()
