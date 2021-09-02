#Resources
#https://makersportal.com/blog/2018/8/23/recording-audio-on-the-raspberry-pi-with-python-and-a-usb-microphone

import struct
import numpy as np
import matplotlib.pyplot as plt
import pyaudio #sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev

print ("done importing")

p = pyaudio.PyAudio()
print("start")

def hw_index():
    count = 0
    with open("usb_devices.txt", 'a+') as myfile:
        for ii in range(p.get_device_count()):
            myfile.write(p.get_device_info_by_index(ii).get('name'))
            myfile.write("\n")

    with open("usb_devices.txt", 'r') as myfile:
        for line  in myfile:
            if "USB" in line:
                print (count)
                break
            count+=1
    return count    

CHUNK = 1024 *4 #how many audio samples
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

#pyaudio object
p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = CHUNK,
    #input_device_index = 0
    )

fig, ax = plt.subplots()

x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))
ax.set_xlim(0, 255)
ax.set_ylim(0, CHUNK)

while True:
    data = stream.read(CHUNK)
    #From binary to int, two times chunk print(len(data))
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'b', data), dtype = 'b')[::2] + 127
    line.set_ydata(data_int)
    fig.canvas.draw()
    fig.canvas.flush_events()
    
