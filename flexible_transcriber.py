import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

class FlexibleTranscriber:
    def __init__(self, engine='google'):
        """initialize wih specified recognizer engine"""
        self.recognizer = sr.Recognizer()
        self.engine = engine
        # optimize settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

        
    def preprocess_audio(self, audio_path):
        """optimize audio for better recognition"""
        audio = AudioSegment.from_file(audio_path)
        # convert to mono and normalize volume
        if audio.channels > 1:
            audio = audio.set_channels(1)
        
        audio = audio.set_frame_rate(16000) # standard sample rate
        audio = audio.normalize() # normalize volume
        # export to tempt wav format
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        audio.export(temp_file.name, format='wav')
        return temp_file

    def transcribe_file(self,  audio_pah, language='en-US'):
        """Transcribe an audio file using the specified engine"""
        preprocessed_path = self.preprocess_audio(audio_pah)
        try:
            with sr.AudioFile(preprocessed_path.name) as source:
               self.recognizer.adjust_for_ambient_noise(source, duration=1)
               audio_data = self.recognizer.record(source)
               
            # perform recognizer
            if self.engine == 'google':
                text =  self.recognizer.recognize_google(audio_data, language=language)
            else:
                text = self.recognizer.recognize_sphinx(audio_data, language=language)
                
            return {
                'text': text,
                'success' : True,
                "engine": self.engine
            }
            
        except sr.UnknownValueError:
            return {
                'text': '',
                'success' : False,
                "engine": self.engine,
                'error': 'Unable to recognize speech'
            }
            
        except sr.RequestError as e:
            return {
                'text': '',
                'success' : False,
                "engine": self.engine,
                'error': f'Request error from {self.engine} service; {str(e)}'
            }
        finally:
            # os.unlink(preprocessed_path)
            pass

if __name__ == '__main__':
    transcriber = FlexibleTranscriber(engine='sphinx')
    result = transcriber.transcribe_file('./resource/jp-1.mp4', language='ja-JP')
    if result['success']:
        print(f"Transcription preview: {result['text'][:200] + '...' if len(result['text']) > 200 else result['text']}")
    else:
        print(f"Error: {result['error']}")
  