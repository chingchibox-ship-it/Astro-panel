import streamlit as st
import os
import glob
from gtts import gTTS

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("⚡ AI Studio Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "mobile":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials.")
else:
    st.title("🎬 Mobile AI Video & TTS Studio")

    CHAR_DIR = "characters"
    os.makedirs(CHAR_DIR, exist_ok=True)

    st.sidebar.header("👤 Characters")
    existing_chars = glob.glob(os.path.join(CHAR_DIR, "*"))
    char_count = len(existing_chars)
    st.sidebar.write(f"Slots filled: **{char_count} / 5**")

    if char_count < 5:
        uploaded_file = st.sidebar.file_uploader("Upload Profile Image", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            with open(os.path.join(CHAR_DIR, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.sidebar.success("Character saved!")
            st.rerun()
    else:
        st.sidebar.warning("❌ Limit reached (Max 5). Delete one to add more.")

    if char_count > 0:
        for char_path in existing_chars:
            name = os.path.basename(char_path)
            if st.sidebar.button(f"🗑️ Remove {name}", key=name):
                os.remove(char_path)
                st.rerun()

    mode = st.radio("Choose Mode:", ["Text to Video", "Image to Video", "Text to Speech (TTS)"])

    selected_char = None
    if char_count > 0:
        char_options = [os.path.basename(p) for p in existing_chars]
        selected_char = st.selectbox("Select Active Character:", char_options)
        st.image(os.path.join(CHAR_DIR, selected_char), width=120)

    prompt = st.text_area("Enter your script / prompt:")

    if st.button("🚀 Process Request"):
        if not prompt:
            st.error("Please enter text first.")
        else:
            with st.spinner("Processing..."):
                if mode == "Text to Speech (TTS)":
                    tts = gTTS(text=prompt, lang='en')
                    tts.save("output.mp3")
                    st.audio("output.mp3")
                    st.success("Audio Created!")
                else:
                    st.info("Mobile Engine Package Output:")
                    st.code(f"MODE: {mode}\nCHARACTER: {selected_char}\nPROMPT: {prompt}")
