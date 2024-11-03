import vosk, wave
import ctypes, os, json, requests, zipfile
import sounddevice as sd
from scipy.io.wavfile import write

model_zip_link="https://alphacephei.com/vosk/models/vosk-model-small-en-in-0.4.zip"

# Creates a Home directory for future functions
work_folder= os.path.join(os.getcwd(), "VOSKMOD")
if not os.path.exists(work_folder):
    os.makedirs(work_folder)

extracted_model= os.path.join(work_folder, "model_extracted")
model_zip_path= os.path.join(work_folder, "model_zip")

# Downloads the Vosk Model
if not os.path.exists(extracted_model):
    if not os.path.exists(model_zip_path):
        model_zip_download=requests.get(model_zip_link)
        with open(model_zip_path,"wb") as file:
            file.write(model_zip_download.content)

    with zipfile.ZipFile(model_zip_path,"r") as file:
        file.extractall(extracted_model)

    os.remove(model_zip_path)

# Makes the working model
model=vosk.Model(os.path.join(extracted_model,"vosk-model-small-en-in-0.4"))
recognizer= vosk.KaldiRecognizer(model, 16000, '["lock"]')

# Records the voice command
duration= 5
rate= 16000
audio= sd.rec(int(duration*rate), samplerate=rate, channels=1, dtype='int16' )
sd.wait()

audio_path= os.path.join(work_folder, "audio.wav")
write(audio_path, rate, audio)

# Recognizes the voice command and carry out the task
with wave.open(audio_path, "rb") as wf:
  while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            if json.loads(result)['text']=="lock":
                ctypes.windll.user32.LockWorkStation()
                break
os.remove(audio_path)
