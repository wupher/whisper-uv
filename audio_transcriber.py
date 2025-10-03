import time
import whisper
import os
from pathlib import Path


class AudioTranscriber:
    def __init__(self, model_size='base'):
        """Initialize transcriber with specified Whisper model"""
        print(f"Loading Whisper model of size: {model_size}")
        self.model = whisper.load_model(model_size)
        print("Model loaded successfully.")

    def transcribe_file(self, audio_path, language=None):
        """
        Transcribe a single audio file to text.

        Args:
            :param audio_path: str Path to the audio file.
            :param language: code ('en', 'es', 'fr', etc.) or None for auto-detect
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"Transcribing audio file: {Path(audio_path).name}")

        start_time = time.time()
        options = {"language": language} if language else {}
        transcribe_result = self.model.transcribe(audio_path, **options)

        processing_time = time.time() - start_time
        print(f"√ Completed in {processing_time:.1f} seconds")
        print(f"Detected language: {transcribe_result['language']}")

        return {
            'text': transcribe_result['text'].strip(),
            'language': transcribe_result['language'],
            'segments': transcribe_result.get('segments', []),
            'processing_time': processing_time
        }

    def save_transcription(self, result_map, output_path):
        """ Save transcription result to a text file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("==== Transcription Result ==== \n")
            f.write(f"Language: {result_map['language']} \n")
            f.write(f"Processing Time: {result_map['processing_time']:.1f} seconds \n")
            f.write("=" * 40 + "\n\n")
            f.write(result_map['text'])
        print(f"Transcription saved to: {output_path}")


def transcribe_audio_file(audio_path, model_size='base', language=None):
    """Simple function to transcribe an audio file"""
    transcriber = AudioTranscriber(model_size=model_size)
    the_result = transcriber.transcribe_file(audio_path, language=language)
    audio_name = Path(audio_path).stem
    output_path = f"{audio_name}_transcription.txt"
    transcriber.save_transcription(the_result, output_path)
    return the_result


if __name__ == "__main__":
    audio_file = "./resource/jp-long.mp3"
    result = transcribe_audio_file(audio_file, model_size='base', language='ja')
    print(f"\nTranscription preview:")
    print(result['text'][:200] + "..." if len(result['text']) > 200 else result['text'])


