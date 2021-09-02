import wave
import numpy as np

test_en_bytes = wave.open("test1.wav","r")

test_en_bytes_wave = test_en_bytes.readframes(-1)
test_fram = test_en_bytes.getframerate()
print("FM es:", test_fram)

en_int = np.frombuffer(test_en_bytes_wave, dtype='int16')


print(test_en_bytes_wave)
print(type(test_en_bytes_wave))
print(len(test_en_bytes_wave))
print("en int es", en_int)
print("en int type es: ", type(en_int))