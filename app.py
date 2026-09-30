import requests
import streamlit as st
import streamlit.components.v1 as components

API_URL = "https://rehab-unpopular-recast.ngrok-free.dev/summarize"   # لينك Ngrok بتاع السيرفر
API_KEY = "secret123"

st.title("🎬 YouTube Video Summarizer")
st.info("This app summarizes **English** YouTube videos only. The video must have English captions.")
video_url = st.text_input("YouTube video link", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Summarize"):
    if not video_url:
        st.warning("Please enter a video link.")
    else:
        if "youtu.be/" in video_url:
            video_id = video_url.split("youtu.be/")[-1].split("?")[0]
        else:
            video_id = video_url.split("v=")[-1].split("&")[0]
        components.iframe(f"https://www.youtube.com/embed/{video_id}", height=315)
        with st.spinner("Summarizing... this may take a few minutes on CPU"):

            try:
                res = requests.post(API_URL, headers={"Authorization": f"Bearer {API_KEY}"},
                                    json={"url": video_url}, timeout=1800)
            except requests.exceptions.RequestException as e:
                st.error(f"Could not reach the server: {e}")
                st.stop()

        if res.status_code == 200:
            result = res.json()
            st.subheader("Summary")
            st.write(result["summary"])
            with st.expander("Detailed summary by section"):
                for i, p in enumerate(result["sections"], 1):
                    st.markdown(f"**{i}.** {p}")
        else:
            st.error(f"Server error {res.status_code}: {res.text[:300]}")