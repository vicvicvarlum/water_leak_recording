#pip install pipwin
#pipwin install pyaudio

#User folder to be created/store the files, dont use blank spaces
user_folder_name = 'wilber2'
#seconds of tolerance to continue adding samples after the threshold has been reached
user_mute_tolerance = 5
#RMS Threshold
THRESHOLD = 0.05
#Min recording lenght (seconds), avoids false triggers
REC_LENGHT = 5

import pyaudio
import wave
import math
import struct
import time
import os, errno
from ftplib import FTP

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 10 # seconds to record
dev_index = 1 # device index found by p.get_device_info_by_index(ii)

errorcount = 0

USER_REC_LENGHT = REC_LENGHT * 100

RATE = 44100  
INPUT_BLOCK_TIME = 0.01
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
SHORT_NORMALIZE = (1.0/32768.0)


audio = pyaudio.PyAudio() # create pyaudio instantiation
# create pyaudio stream
#domain name or server ip:
ftp = FTP('ftp.lumenir-innovations.com')

def placeFile(myfile):

    print(ftp.storbinary('STOR '+myfile, open(myfile, 'rb')))


def find_input_device():
    device_index = None            
    for i in range( audio.get_device_count() ):     
        devinfo = audio.get_device_info_by_index(i)   
        print( "Device %d: %s"%(i,devinfo["name"]) )

        for keyword in ["mic","HiFiBerry"]:
            if keyword in devinfo["name"].lower():
                print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                device_index = i
                return device_index

    if device_index == None:
        print( "No preferred input found; using default input device." )

    return device_index

stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = find_input_device(),input = True, \
                    frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

try:
    os.makedirs(user_folder_name)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

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
count = 0 # loop iteration 

seconds_to_sample = 20 * 100 #in seconds first arg

mute_tolerance = user_mute_tolerance * 100 +100 #seconds // Added +100 to downcount including starting point

append_samples = False

build_new_file_exists = False

filename_audio = ""

dots_mute_tolerance_counter = 0
dots_total_seconds = int(mute_tolerance/100)

count_when_trigger = 0
count_when_trigger_dots = 0

print (ftp.login(user='waterleak@lumenir-innovations.com', passwd = 'Lumen!r710!'))
data = []
ftp.dir(data.append)


create_ftp_user_folder = False

for line in data:
    print ("-", line)
    if user_folder_name in line:
        print ("User folder exists, folder will not be created")
        create_ftp_user_folder = False
    else:
        create_ftp_user_folder = True


if create_ftp_user_folder:
    print ('User folder doesnt exists, creating',user_folder_name,'folder')
    print (ftp.mkd(user_folder_name))
    create_ftp_user_folder = False

ftp.cwd('/'+user_folder_name+'/')

while True:

    try:
        data = stream.read(INPUT_FRAMES_PER_BLOCK, exception_on_overflow = False)
    except IOError as e:
        # dammit. 
        errorcount += 1
        print( "(%d) Error recording: %s"%(errorcount,e) )

    #Convert from bytes to int and calculate RMS value of the samples
    rms_val = get_rms(data)

    if append_samples == False:
        count = 0

    if(rms_val > THRESHOLD):

        if(build_new_file_exists == False):
            filename_audio = time.ctime().replace(" ","").replace(":","_") + "_sample.wav"
            print("File name started: ", filename_audio)
            build_new_file_exists = True

        print("T", count, rms_val)
        #Used for mute tolerance calculation
        count_when_trigger = count
        #Used for down counter
        count_when_trigger_dots = count
        #Proceed with storing the samples
        append_samples = True

        

    #Continue to append the samples to the list even when we havent met the threshold (on mute)
    if(append_samples == True and (count <= count_when_trigger + mute_tolerance )) :
        frames.append(data)
        if(count > count_when_trigger_dots+100 ):
            count_when_trigger_dots = count 
            dots_mute_tolerance_counter +=1
            print(dots_total_seconds-dots_mute_tolerance_counter, end=' ', flush=True)

        

    if(count > count_when_trigger + mute_tolerance and len(frames)!= 0):
        if count-mute_tolerance > USER_REC_LENGHT:
            append_samples = False
            # save the audio frames as .wav file
            wavefile = wave.open(filename_audio,'wb')
            #wavefile = wave.open(user_folder_name+'/'+filename_audio,'wb')
            wavefile.setnchannels(chans)
            wavefile.setsampwidth(audio.get_sample_size(form_1))
            wavefile.setframerate(samp_rate)
            wavefile.writeframes(b''.join(frames))
            wavefile.close()
            print("New file saved: ", filename_audio, count)
            print(placeFile(filename_audio))


            frames.clear()
            build_new_file_exists = False
            count = 0
            dots_mute_tolerance_counter = 0
        else:
            print("No file created, false trigger", count)
            frames.clear()
            build_new_file_exists = False
            count = 0
            dots_mute_tolerance_counter = 0
            append_samples = False

    count +=1
    #if(count >seconds_to_sample):
        
    

print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()
ftp.quit()



