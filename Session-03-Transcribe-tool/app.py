import streamlit as st
import whisper
import tempfile

st.title("🎙️ Audio Transcriber (Free, Local Whisper)")

model = whisper.load_model("base")  # tiny, base, small, medium, large

file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a", "ogg"])

if file and st.button("Transcribe"):
    with st.spinner("Transcribing..."):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(file.getvalue())
            tmp_path = tmp.name
        result = model.transcribe(tmp_path)
    st.write(result["text"])