import streamlit as st
from PIL import Image
import base64
import time
import os
import base64
import streamlit as st
import streamlit.components.v1 as components

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

if 'current_rank' not in st.session_state:
    st.session_state.current_rank = "D Rank"  # Default rank, can be updated later

if 'RANK_IMAGES' not in st.session_state:
    st.session_state.RANK_IMAGES = {
        "S Rank": "images/s_rank.png",
        "A Rank": "images/a_rank.png",
        "B Rank": "images/b_rank.png",
        "C Rank": "images/c_rank.png",
        "D Rank": "images/d_rank.png",
        "E Rank": "images/e_rank.png",
        "F Rank": "images/f_rank.png"
    }

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

if(not st.session_state.disable_button):
  # --- Trigger Button (always visible) ---
  if st.button("Take Hunter Rank Assessment", key="hunter_rank_assessment", type="primary", disabled=st.session_state.disable_button) or st.session_state.taking_assessment:
      
      st.session_state.taking_assessment = True

      # --- Character Selection (only after button click) ---
      choice = st.selectbox("Choose your character:", ["-- Select Character ⚔️ --", "Parth Dhawan"])
      st.session_state.character = choice

      if st.session_state.character != "-- Select Character ⚔️ --":
          # --- Rank Config ---
          

          if not st.session_state.assessment_completed:
            st.write("1️⃣ Assessing Physical Prowess")
            bar1 = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                bar1.progress(i + 1)
            st.success("⚔️ Physical Prowess Assessed!")

            st.write("2️⃣ Analyzing Combat Skills")
            bar2 = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                bar2.progress(i + 1)
            st.success("🎯 Combat Skills Analyzed!")

            st.write("3️⃣ Calibrating Magical Aura")
            bar3 = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                bar3.progress(i + 1)
            st.success("🌌 Magical Aura Calibrated!")

            st.write("✅ All systems complete. Your Hunter rank has been updated!")
            st.session_state.assessment_completed = True
            st.session_state.disable_button = True  # Disable button after click 
            with st.spinner("Please wait..."):
              time.sleep(5)
            st.rerun()
else:

  
  custom_labels = {
      "s_rank.png":      "S Rank", 
      "s_rank_locked.png": "S Rank (Locked)",
      "a_rank.png":      "A Rank",
      "a_rank_locked.png": "A Rank (Locked)",
      "b_rank.png":      "B Rank",
      "b_rank_locked.png": "B Rank (Locked)",
      "c_rank.png":      "C Rank",
      "c_rank_locked.png": "C Rank (Locked)",
      "d_rank.png":      "D Rank",
      "d_rank_locked.png": "D Rank (Locked)",
      "e_rank.png":      "E Rank",
      "e_rank_locked.png": "E Rank (Locked)",
      # add more mappings as needed...
  }

  # We explicitly list them in the order we want to appear:
  filenames_in_order = [
      "e_rank.png",
      "d_rank.png",
      "c_rank_locked.png",
      "b_rank_locked.png",
      "a_rank_locked.png",
      "s_rank_locked.png",
  ]

  # Verify they exist on disk / warn if missing
  IMAGES_DIR = "images"
  missing = [fn for fn in filenames_in_order if not os.path.isfile(os.path.join(IMAGES_DIR, fn))]
  if missing:
      st.error(f"The following files were not found in `{IMAGES_DIR}/`: {missing}")
      st.stop()

  # Build two parallel lists: one for data‐URIs, one for labels
  image_data_uris = []
  labels = []
  for fname in filenames_in_order:
      full_path = os.path.join(IMAGES_DIR, fname)
      # 1A) Read and base64‐encode
      with open(full_path, "rb") as f:
          raw = f.read()
      b64 = base64.b64encode(raw).decode("utf-8")
      data_uri = f"data:image/png;base64,{b64}"
      image_data_uris.append(data_uri)
      # 1B) Fetch the custom label from our dict (must exist)
      labels.append(custom_labels[fname])

  # ─── 2) BUILD HTML SLIDES (IMG + CUSTOM LABEL) ──────────────────────────────
  slide_blocks = []
  for uri, lbl in zip(image_data_uris, labels):
      slide_blocks.append(
          f"""
          <div class="swiper-slide">
            <div class="slide-content">
              <img src="{uri}" />
              <div class="caption">{lbl}</div>
            </div>
          </div>
          """
      )

  slides_html = "\n".join(slide_blocks)

  carousel_html = f"""
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"
  />

  <style>
    /* ── CONTAINER ── */
    .swiper {{
      width: 100%;
      padding-top: 50px;
      padding-bottom: 50px;
    }}

    /* ── EACH SLIDE (wrapper) ── */
    .swiper-slide {{
      background: none;
      width: 200px;
    }}

    /* ── INNER CONTENT (image + label) ── */
    .slide-content {{
      display: flex;
      flex-direction: column;
      align-items: center;
    }}

    /* ── IMAGE (circle) ── */
    .slide-content img {{
      width: 180px;
      height: 180px;
      border-radius: 90px;
      object-fit: cover;
      transition: transform 0.3s ease, filter 0.3s ease;
      filter: grayscale(80%) brightness(60%);
    }}

    /* ── LABEL UNDER IMAGE ── */
    .slide-content .caption {{
      margin-top: 0px;
      font-size: 15px;
      color: #000;
      text-align: center;
      border: 2px solid #000;
      padding: 4px 8px;
      border-radius: 4px;
      display: inline-block;
      background-color: rgba(255, 255, 255, 0.4);
      z-index: 10;
    }}

    /* ── ACTIVE (center) SLIDE IMAGE ── */
    .swiper-slide-active .slide-content img {{
      filter: none;
      transform: scale(1.5);
      z-index: 2;
    }}

    /* ── NAVIGATION ARROWS ── */
    .swiper-button-next,
    .swiper-button-prev {{
      color: #fff;
      width: 44px;
      height: 44px;
    }}
    .swiper-button-next::after,
    .swiper-button-prev::after {{
      font-size: 1.5rem;
    }}

    /* ── DISABLED “Prev” STATE ── */
    .swiper-button-prev.disabled {{
      opacity: 0.3;
      pointer-events: none;
    }}
  </style>

  <div class="swiper">
    <div class="swiper-wrapper">
      {slides_html}
    </div>
    <div class="swiper-button-prev"></div>
    <div class="swiper-button-next"></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
  <script>
    const swiper = new Swiper('.swiper', {{

      effect: 'coverflow',
      grabCursor: true,
      centeredSlides: true,
      slidesPerView: 'auto',
            // start with the first slide
      loop: false,                  // do not loop so there's a real first slide
      allowSlidePrev: true,        // disable left-swipe on first slide
      coverflowEffect: {{
        rotate: 30,
        stretch: 0,
        depth: 150,
        modifier: 1.5,
        slideShadows: true,
      }},
      navigation: {{
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      }},

    }});
    swiper.slideNext(0, false);
  </script>
  """




    
  # Display Rank & Image
  st.markdown(f"### Current Rank: **{st.session_state.current_rank }**")


    # ─── 3) RENDER THE CAROUSEL ─────────────────────────────────────────────────
  components.html(carousel_html, height=300)

  img = Image.open(st.session_state.RANK_IMAGES[st.session_state.current_rank ])
  # st.image(img, width=600, caption=f"Rank: {st.session_state.current_rank }", use_container_width=True)

  st.markdown("#### You are an Assassin 🥷 type hunter!")
  # Motivational Message
  # st.info("Be disciplined, focused, and never give up!")
  # st.info("Just like Sung Jinwoo, every practice session makes you stronger!")
  st.info("Congratulations Hunter, You are not the weakest now!")
