import numpy as np
from scipy.io import wavfile

def create_bell_sound():
    # ベル音（柔らかい音）を生成
    sample_rate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    frequency = 440
    signal = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 3)
    signal = signal * 0.3  # 音量調整
    wavfile.write("bell.wav", sample_rate, (signal * 32767).astype(np.int16))

def create_alarm_sound():
    # アラーム音（やや強い音）を生成
    sample_rate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    frequency = 880
    signal = np.sin(2 * np.pi * frequency * t)
    signal = signal * 0.5  # 音量調整
    wavfile.write("alarm.wav", sample_rate, (signal * 32767).astype(np.int16))

if __name__ == "__main__":
    create_bell_sound()
    create_alarm_sound() 