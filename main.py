import streamlit as st
import wikipedia
import os
from groq import Groq
from dotenv import load_dotenv

# API Key load
load_dotenv()

# 1. Page Config
st.set_page_config(page_title="Query-Match AI", layout="wide")

# --- GROQ API SETUP ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

LOGO_FILE = 'maxresdefault-removebg-preview (1).png'

# --- CHAT HISTORY INITIALIZATION ---
if 'active' not in st.session_state: 
    st.session_state.active = False
if 'history' not in st.session_state:
    st.session_state.history = []

# 2. Professional UI CSS
st.markdown("""
    <style>
    .stApp { background: #000000 !important; }
    .featured-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px; padding: 30px;
        border-left: 5px solid #00f2ff; margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0, 242, 255, 0.1);
    }
    .result-link { color: #8ab4f8; font-size: 22px; text-decoration: none; font-weight: bold; }
    .name-tag { color: #ccff00; font-size: 22px; font-weight: bold; text-align: center; text-shadow: 0 0 10px #ccff00; }
    
    /* Centering all main text elements */
    .center-text { text-align: center !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# ==================== HOME PAGE (CENTERED LAYOUT) ====================
    # ==================== HOME PAGE (CENTERED & GAP FIX) ====================
if not st.session_state.active:
    # 1. Spacing for Vertical Center
    for _ in range(4): 
        st.write("") 

    # 2. Layout Column
    _, col, _ = st.columns([0.1, 5, 0.1])
    
    with col:
        # --- LOGO BLOCK ---
        try:
            st.image(LOGO_FILE, use_container_width=True)
            
            # 3. DEPARTMENT NAME (Gap fix using negative margin)
            # margin-top: -180px gap ni thaggisthundhi
            st.markdown("""
                <div style='text-align: center;'>
                    <p style='color: #FFDF00; font-size: clamp(20px, 4vw, 32px); font-weight: bold; 
                    margin-top: -180px; margin-bottom: 0px;'>
                        DEPARTMENT OF ARTIFICIAL INTELLIGENCE & DATA SCIENCE
                    </p>
                    <hr style='margin: 15px auto; width: 80%; border: 0.5px solid #444;'>
                </div>
            """, unsafe_allow_html=True)
        except:
            st.markdown("<h1 style='text-align: center; color: #ff9900;'>RC</h1>", unsafe_allow_html=True)

        # 4. PROJECT TITLE (Responsive Middle)
        # clamp function valla font size phone lo chinnadhi, PC lo peddhadi avthundhi
        st.markdown("""
            <div style='text-align: center; width: 100%;'>
                <h1 style='color: white; letter-spacing: 4px; font-size: clamp(40px, 7vw, 75px); 
                margin-top: 10px; font-weight: 800;'>
                    🧠 QUERY-MATCH AI
                </h1>
            </div>
        """, unsafe_allow_html=True)

        # 5. DESIGNERS BOX (Colors & Font Same for all)
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.03); padding: 25px; border-radius: 20px; 
            border: 1px solid #444; margin-top: 30px; text-align: center;'>
                <p style='color: #8ab4f8; font-weight: bold; margin-bottom: 5px; font-size: 14px;'>PROJECT BY</p>
                <div class='name-tag' style='font-size: clamp(18px, 3vw, 24px);'>
                    SUMA SREE | JHANSI TANUJA | NAVYA SRI
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.write("")
        # 6. LAUNCH BUTTON
        if st.button("LAUNCH SEARCH 🚀", use_container_width=True):
            st.session_state.active = True
            st.rerun()
      

# ==================== SEARCH PAGE ====================
else:
    # --- CHAT HISTORY SIDEBAR ---
    with st.sidebar:
        st.markdown("<h2 style='color: #00f2ff;'>📜 Search History</h2>", unsafe_allow_html=True)
        st.write("---")
        
        if st.session_state.history:
            for item in reversed(st.session_state.history):
                st.info(f"🔍 {item}")
            
            st.write("---")
            if st.button("Clear History 🗑️"):
                st.session_state.history = []
                st.rerun()
        else:
            st.write("No history yet.")
            
        st.write("---")
        st.sidebar.button("⬅️ Back Home", on_click=lambda: st.session_state.update({"active": False}))

    h_col1, h_col2 = st.columns([1, 4])
    with h_col1:
        try:
            st.image(LOGO_FILE, width=120)
        except:
            st.markdown("<h2 style='color:#ff9900;'>RC</h2>", unsafe_allow_html=True)
    with h_col2:
        st.markdown("<h2 style='color:#00f2ff; margin-top: 20px;'>QUERY-MATCH SEARCH INTERFACE</h2>", unsafe_allow_html=True)
    
    query = st.text_input("", placeholder="Search anything (Ex: Artificial Intelligence, NASA, Python)...")

    if query:
        # Save query to history if it's new
        if query not in st.session_state.history:
            st.session_state.history.append(query)

        with st.spinner('Unifying Query Nodes...'):
            try:
                # AI Unification Logic (Groq)
                if client:
                    chat = client.chat.completions.create(
                        messages=[{"role": "user", "content": f"Provide a concise semantic overview of: {query}"}],
                        model="llama-3.3-70b-versatile",
                    )
                    ai_res = chat.choices[0].message.content

                    st.markdown(f"""
                        <div class='featured-box'>
                            <div style='color: #00f2ff; font-size: 14px; font-weight: bold;'>UNIFIED INSIGHT: {query.upper()}</div>
                            <div style='color: white; font-size: 19px; line-height: 1.8; margin-top: 15px;'>
                                {ai_res}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                # Wikipedia Related Nodes
                search_list = wikipedia.search(query, results=5)
                if search_list:
                    st.write("<p style='color:#bdc1c6; font-size: 18px; font-weight: bold;'>Related Semantic Nodes:</p>", unsafe_allow_html=True)
                    for title in search_list:
                        u = f"https://www.google.com/{title.replace(' ', '_')}"
                        st.markdown(f"**[{title}]({u})**")
            except Exception as e:
                st.error(f"Error: {e}")