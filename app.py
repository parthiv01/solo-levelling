import streamlit as st
from PIL import Image
import base64
import time

# --- Page config ---
st.set_page_config(layout="wide", page_title="Solo Math Levelling")

if "character" not in st.session_state:
    st.session_state.character = None

if "taking_assessment" not in st.session_state:
    st.session_state.taking_assessment = False

if 'disable_button' not in st.session_state:
    st.session_state.disable_button = False

if 'assessment_completed' not in st.session_state:
    st.session_state.assessment_completed = False

# --- Helper to set a local background image ---
def set_bg_local(image_path: str):
    with open(image_path, "rb") as img_file:
        b64_bytes = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
      .stApp {{
        background-image: url("data:image/png;base64,{b64_bytes}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
      }}
      /* Optional: make content boxes semi-transparent */
      .css-18e3th9, .css-1d391kg {{
        background-color: rgba(255, 255, 255, 0.8);
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_bg_local("images/bg.png")

# --- App Header (always visible) ---
st.title("📈 Solo Math Levelling")

# --- Trigger Button (always visible) ---
if st.button("Take Hunter Rank Assessment", key="hunter_rank_assessment", type="primary", disabled=st.session_state.disable_button) or st.session_state.taking_assessment:
    st.session_state.disable_button = True  # Disable button after click 
    st.session_state.taking_assessment = True

    # --- Character Selection (only after button click) ---
    choice = st.selectbox("Choose your character:", ["-- Select Character ⚔️ --", "Parth Dhawan"])
    st.session_state.character = choice

    if st.session_state.character != "-- Select Character ⚔️ --":
        # --- Rank Config ---
        RANK_IMAGES = {
            "F Rank": "images/f_rank.png",
            "E Rank": "images/e_rank.jpg",
            "D Rank": "images/d_rank.png",
            "C Rank": "images/c_rank.png",
            "B Rank": "images/b_rank.png",
            "A Rank": "images/a_rank.png",
            "S Rank": "images/s_rank.png"
        }
        current_rank = "E Rank"  # fetch from your backend in reality

        if not st.session_state.assessment_completed:
          st.write("1️⃣ Assessing Physical Prowess")
          bar1 = st.progress(0)
          for i in range(100):
              time.sleep(0.03)
              bar1.progress(i + 1)
          st.success("⚔️ Physical Prowess Assessed!")

          st.write("2️⃣ Analyzing Combat Skills")
          bar2 = st.progress(0)
          for i in range(100):
              time.sleep(0.03)
              bar2.progress(i + 1)
          st.success("🎯 Combat Skills Analyzed!")

          st.write("3️⃣ Calibrating Magical Aura")
          bar3 = st.progress(0)
          for i in range(100):
              time.sleep(0.03)
              bar3.progress(i + 1)
          st.success("🌌 Magical Aura Calibrated!")

          st.write("✅ All systems complete. Your Hunter rank has been updated!")
          st.session_state.assessment_completed = True
          with st.spinner("Please wait..."):
            time.sleep(5)
          st.rerun()
        else:
            
          # Display Rank & Image
          st.markdown(f"### Assessed Rank: **{current_rank}**")
          st.markdown("#### You are an Assassin 🥷 type hunter!")

          img = Image.open(RANK_IMAGES[current_rank])
          st.image(img, width=600, caption=f"Rank: {current_rank}", use_container_width=True)

          # Motivational Message
          # st.info("Be disciplined, focused, and never give up!")
          st.info("Just like Sung Jinwoo, every practice session makes you stronger!")
