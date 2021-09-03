#pip install pipwin
#pipwin install pyaudio

from typing import Tuple
import pyaudio
import wave
import math
import struct
import time

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 10 # seconds to record
dev_index = 1 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file

wav_output_filename2 = 'tt1.wav' # name of .wav file

print(type(wav_output_filename2))

RATE = 44100  
INPUT_BLOCK_TIME = 0.01
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
SHORT_NORMALIZE = (1.0/32768.0)


audio = pyaudio.PyAudio() # create pyaudio instantiation
# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

frames = []

def get_rms(block):


    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    sum_squares = 0.0
    for sample in shorts:
    # sample is a signed short in +/- 32768. 
    # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )


rms_val = 0.0 #Placeholder to store rms converted val from chunk*sample_rate
THRESHOLD = 0.03 #RMS Threshold for recording
count = 0 # loop iteration 

seconds_to_sample = 20 * 100 #in seconds first arg

threshold_flag = False
mute_tolerance = 5 * 100 #seconds 
threshold_flag_when_trigger = 0
append_en_timeout = False

build_new_file_exists = False

filename_audio = ""

print(filename_audio)
print(type(filename_audio))
while True:
    
    data = stream.read(INPUT_FRAMES_PER_BLOCK)
    rms_val = get_rms(data)
    
    #print(rms_val, count)

    if(rms_val > THRESHOLD):
        print("T", count, rms_val)
        frames.append(data)
        threshold_flag_when_trigger = count
        threshold_flag = True
        append_en_timeout = True

        if(build_new_file_exists == False):
            filename_audio = time.ctime().replace(" ","").replace(":","_") + "_sample.wav"
            print("New file started: ", filename_audio)
            build_new_file_exists = True
    else:
        threshold_flag = False

    if(threshold_flag == True): ##check so not duplicate samples are stored 
        None
    elif(append_en_timeout == True and (count <= threshold_flag_when_trigger + mute_tolerance )) :
        frames.append(data)

    if(count > threshold_flag_when_trigger + mute_tolerance):
        append_en_timeout = False
        # save the audio frames as .wav file
        print("New file saved: ", filename_audio)
        wavefile = wave.open(filename_audio,'wb')
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(audio.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()
        frames.clear()
        build_new_file_exists = False
        count = 0

    count +=1
    #if(count >seconds_to_sample):
        
    

print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()



