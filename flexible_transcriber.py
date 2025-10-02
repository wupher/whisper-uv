import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

class FlexibleTranscriber:
    def __init__(self, engine='google'):
        """initialize wih specified recoginzer engine"""
        self.recoginzer = sr.Recognizer()
        self.engine = engine
        # optimize settings
        self.recoginzer.energy_threshold = 300
        self.recoginzer.dynamic_energy_threshold = True

        
    def preprocess_audio(self, audio_path):
        """optimize audo for better recognition"""
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
               self.recoginzer.adjust_for_ambient_noise(source, duration=1)
               audio_data = self.recoginzer.record(source)
               
            # perform recoginzer
            if self.engine == 'google':
                text =  self.recoginzer.recoginze_google(audio_data, language=language)
            elif self.engine == 'sphinx':
                text = self.recoginzer.recognize_sphinx(audio_data, language=language)
                
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
            os.unlink(preprocessed_path)

def __main__():
    transcriber = FlexibleTranscriber(engine='google')
    result = transcriber.transcribe_file('sample_audio.wav', language='en-US')
  