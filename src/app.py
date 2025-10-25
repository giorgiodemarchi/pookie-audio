import streamlit as st
import tempfile
import os
from transcription import transcribe_audio

st.set_page_config(
    page_title="Pookie Audio Transcription",
    page_icon="🎵",
    # layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    /* Mobile-first responsive design */
    @media (max-width: 767px) {
        /* Make main content full width on mobile */
        .main .block-container {
            padding: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Larger touch targets */
        .stButton > button {
            width: 100% !important;
            height: 48px !important;
            font-size: 16px !important;
            margin: 8px 0 !important;
        }
        
        /* Better file uploader on mobile */
        .stFileUploader {
            border: 2px dashed #ccc !important;
            border-radius: 8px !important;
            padding: 20px !important;
            text-align: center !important;
        }
        
        /* Responsive columns */
        .stColumns > div {
            flex-direction: column !important;
        }
        
        /* Better text areas on mobile */
        .stTextArea textarea {
            font-size: 16px !important;
            min-height: 120px !important;
        }
        
        /* Mobile-friendly expanders */
        .streamlit-expanderHeader {
            font-size: 18px !important;
            padding: 12px !important;
        }
    }
    
    /* Desktop optimizations */
    @media (min-width: 768px) {
        .main .block-container {
            max-width: 1200px !important;
            padding: 2rem !important;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Pookie Audio Transcription")
st.markdown("Upload up to 5 audio files to get their transcriptions.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Upload Audio Files")
    st.markdown("**Supported formats:** MP3, WAV, M4A, FLAC, AAC, OGG")

with col2:
    st.markdown("**Tip:** Tap and hold to select multiple files on mobile")

uploaded_files = st.file_uploader(
    "Choose audio files",
    type=["mp3", "wav", "m4a", "flac", "aac", "ogg"],
    accept_multiple_files=True,
    help="You can upload up to 5 audio files at once",
    label_visibility="collapsed",
)

if uploaded_files and len(uploaded_files) > 5:
    st.error("Please upload no more than 5 files at once.")
    uploaded_files = uploaded_files[:5]


if uploaded_files:
    st.header(f"Transcriptions ({len(uploaded_files)} files)")
    total_size = sum(f.size for f in uploaded_files) / 1024 / 1024
    st.info(f"Total files: {len(uploaded_files)} | Total size: {total_size:.1f} MB")

    for i, uploaded_file in enumerate(uploaded_files, 1):
        with st.expander(f"{uploaded_file.name}", expanded=True):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.metric("Size", f"{uploaded_file.size / 1024:.1f} KB")
            with col2:
                st.metric("Type", uploaded_file.type.split("/")[-1].upper())
            with col3:
                st.metric("File", f"#{i}")

            with tempfile.NamedTemporaryFile(
                delete=False, suffix=f"_{uploaded_file.name}"
            ) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            if st.button(
                f"Transcribe {uploaded_file.name}",
                key=f"transcribe_{i}",
                type="primary",
                use_container_width=True,
            ):
                try:
                    with st.spinner(
                        f"Transcribing {uploaded_file.name}... This may take a few minutes."
                    ):
                        transcript = transcribe_audio(tmp_file_path)

                        st.success("Transcription completed!")

                        st.subheader("Transcript")
                        st.text_area(
                            f"Transcript for {uploaded_file.name}:",
                            value=transcript,
                            height=200,
                            key=f"transcript_{i}",
                            placeholder="Your transcript will appear here...",
                        )

                        # Download button
                        col_download, col_copy = st.columns([1, 1])
                        with col_download:
                            st.download_button(
                                label="Download Transcript",
                                data=transcript,
                                file_name=f"{uploaded_file.name}_transcript.txt",
                                mime="text/plain",
                                key=f"download_{i}",
                                use_container_width=True,
                            )
                        with col_copy:
                            if st.button(
                                "Copy to Clipboard",
                                key=f"copy_{i}",
                                use_container_width=True,
                            ):
                                st.code(transcript, language=None)

                except Exception as e:
                    st.error(f"Error transcribing {uploaded_file.name}: {str(e)}")

                finally:
                    if os.path.exists(tmp_file_path):
                        os.unlink(tmp_file_path)

            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

else:
    st.markdown("---")
    st.info("Upload audio files above to get started!")


st.markdown("---")
st.markdown("**Built by Luigi with ❤️** | **Powered by OpenAI Whisper**")
