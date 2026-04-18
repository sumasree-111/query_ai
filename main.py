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
# ==================== HOME PAGE (BALANCED PC & MOBILE) ====================
if not st.session_state.active:
    # 1. Custom CSS for Perfect Gap Control
    st.markdown("""
        <style>
        /* Mobile vs PC Alignment */
        .home-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding-top: 5vh;
        }
        
        .responsive-logo {
            width: 100%;
            max-width: 550px;
            height: auto;
            margin-bottom: -5%; /* Dynamic gap based on screen size */
        }

        .dept-text {
            color: #FFDF00;
            font-weight: bold;
            font-size: clamp(16px, 2.5vw, 28px);
            margin-top: -80px; /* Base gap fix */
            line-height: 1.2;
            z-index: 10;
        }

        /* Adjustments for Mobile specifically */
        @media screen and (max-width: 600px) {
            .dept-text {
                margin-top: -40px !important; /* Mobile lo logo paiki vellakunda adjustment */
                font-size: 16px;
            }
            .responsive-logo {
                max-width: 300px;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. Layout
    _, col, _ = st.columns([0.1, 5, 0.1])
    
    with col:
        # LOGO & DEPT NAME (Using HTML for better gap control)
        st.markdown(f"""
            <div class="home-container">
                <img src="https://raw.githubusercontent.com/user-attachments/assets/logo_file" class="responsive-logo">
                <p class="dept-text">DEPARTMENT OF ARTIFICIAL INTELLIGENCE & DATA SCIENCE</p>
                <hr style="width: 70%; border: 0.5px solid #444; margin: 15px auto;">
            </div>
        """, unsafe_allow_html=True)
        
        # Local Logo Fallback (If HTML image doesn't load)
        try:
             st.image(LOGO_FILE, use_container_width=True)
        except:
             pass

        # PROJECT TITLE
        st.markdown("""
            <div style='text-align: center; margin-top: 10px;'>
                <h1 style='color: white; letter-spacing: 2px; font-size: clamp(35px, 6vw, 65px); font-weight: 800;'>
                    🧠 QUERY-MATCH AI
                </h1>
            </div>
        """, unsafe_allow_html=True)

        # DESIGNERS BOX
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.03); padding: 20px; border-radius: 15px; 
            border: 1px solid #444; margin-top: 25px; text-align: center;'>
                <p style='color: #8ab4f8; font-weight: bold; margin-bottom: 5px; font-size: 14px;'>PROJECT BY</p>
                <div style='color: #ccff00; font-weight: bold; font-size: clamp(16px, 2.5vw, 24px);'>
                    SUMA SREE | JHANSI TANUJA | NAVYA SRI
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.write("")
        # LAUNCH BUTTON
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