from src.transcription import transcribe_audio
import argparse


def main(file_path: str):
    print("Hello from pookie-audio!")
    transcript = transcribe_audio(file_path)
    print(transcript)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pookie Audio Transcription")
    parser.add_argument(
        "file_path", type=str, help="The path to the audio file to transcribe"
    )
    args = parser.parse_args()
    main(args.file_path)
