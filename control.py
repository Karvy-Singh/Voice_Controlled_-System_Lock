import vosk, wave
import ctypes, shutil, os, json
from vosk import Model, KaldiRecognizer
import sounddevice as sd
from scipy.io.wavfile import write, read
