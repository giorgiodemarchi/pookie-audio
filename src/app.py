from streamlit.runtime.uploaded_file_manager import UploadedFile


import streamlit as st
import tempfile
import os
from transcription import transcribe_audio

st.set_page_config(
    page_title="Pookie Audio Transcription",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .css-1d391kg {
        width: 600px !important;
    }
    .css-1cypcdb {
        width: 600px !important;
    }
    section[data-testid="stSidebar"] {
        width: 600px !important;
    }
    section[data-testid="stSidebar"] > div {
        width: 600px !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Pookie Audio Transcription")
st.markdown("Upload up to 5 audio files to get their transcriptions.")

with st.sidebar:
    st.header("Upload Audio Files")
    st.markdown("**Supported formats:** MP3, WAV, M4A, FLAC, etc.")

    uploaded_files = st.file_uploader(
        "Choose audio files",
        type=["mp3", "wav", "m4a", "flac", "aac", "ogg"],
        accept_multiple_files=True,
        help="You can upload up to 5 audio files at once",
    )

    if uploaded_files and len(uploaded_files) > 5:
        st.error("Please upload no more than 5 files at once.")
        uploaded_files = uploaded_files[:5]

if uploaded_files:
    st.header(f"Transcriptions ({len(uploaded_files)} files)")

    for i, uploaded_file in enumerate[UploadedFile](uploaded_files, 1):
        with st.expander(f"{uploaded_file.name}", expanded=True):
            col1, col2 = st.columns([1, 3])

            with col1:
                st.write(f"Size: {uploaded_file.size / 1024:.1f} KB")
                st.write(f"Type: {uploaded_file.type}")

            with col2:
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=f"_{uploaded_file.name}"
                ) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                if st.button(f"Transcribe {uploaded_file.name}", key=f"transcribe_{i}"):
                    try:
                        with st.spinner(f"Transcribing {uploaded_file.name}..."):
                            transcript = transcribe_audio(tmp_file_path)

                            st.success("Transcription completed!")
                            st.text_area(
                                f"Transcript for {uploaded_file.name}:",
                                value=transcript,
                                height=150,
                                key=f"transcript_{i}",
                            )

                            st.download_button(
                                label=f"Download {uploaded_file.name} transcript",
                                data=transcript,
                                file_name=f"{uploaded_file.name}_transcript.txt",
                                mime="text/plain",
                                key=f"download_{i}",
                            )

                    except Exception as e:
                        st.error(f"Error transcribing {uploaded_file.name}: {str(e)}")

                    finally:
                        if os.path.exists(tmp_file_path):
                            os.unlink(tmp_file_path)

                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)

else:
    st.info("Please upload audio files using the sidebar to get started!")


st.markdown("---")
st.markdown("Built by Luigi with ❤️")
