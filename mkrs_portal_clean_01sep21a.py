#pip install pipwin
#pipwin install pyaudio

import pyaudio
import wave
import numpy as np
import struct
import matplotlib.pyplot as plt
import math

def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

RATE = 44100  
INPUT_BLOCK_TIME = 0.01
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
SHORT_NORMALIZE = (1.0/32768.0)

TIMEOUT_S = 5

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 0.05 # seconds to record
dev_index = 5 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=INPUT_FRAMES_PER_BLOCK)
print("recording")
frames = []



# loop through stream and append audio chunks to frame array
#for ii in range(0,int((samp_rate/chunk)*record_secs)):
#    data = stream.read(chunk)
#    data_int = np.frombuffer(data, dtype='int16')
#    frames.append(data)
count = 0
rms_vals = []
x_rms_vals = []

int_vals_16 = []

recording_append = False
count_when_trigger = 0
count_when_trigger_flag = False

while True:
    data = stream.read(INPUT_FRAMES_PER_BLOCK)
    data_int = np.frombuffer(data, dtype='int16')
    
    #int_vals_16.append(data_int)
    my_rms_val = get_rms(data)
    
    if(my_rms_val > .01):
        recording_append = True
        count_when_trigger = count
        count_when_trigger_flag = True
    else:
        recording_append = False
        
    if(recording_append == False and count_when_trigger_flag == True):
        if ( (count_when_trigger + TIMEOUT_S) >= count):
            recording_append = True
        else:
            recording_append = False
            
            
    if recording_append:
        frames.append(data)
    
    rms_vals.append(my_rms_val)
    print(my_rms_val, " ", count)
    
    x_rms_vals.append(count)    
    count+=1
    if(my_rms_val > 0.19):
        print("Over 0.1")
        #break
    if(count >2000
       ):
        break

print("Len int_vals_16 total: ", len(int_vals_16))
#print(int_vals_16[0])
#print("Len int_vals_16 pos [0]: ",len(int_vals_16[0]))
#print("Len int_vals_16 pos [1]: ",len(int_vals_16[1]))
#print("Len int_vals_16 pos [101]: ",len(int_vals_16[101-1]))

    #print (data)
    #print (data_int)
    #print ("max data_int", max(data_int))
    #print ("min data_int", min(data_int))
    #break
    


# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

plt.title("Byte to Int16")
plt.plot(x_rms_vals, rms_vals)
plt.show()

#data = stream.read(chunk)
#data_int = int.from_bytes(data,"big")
#frames.append(data)

print("finished recording")



# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()