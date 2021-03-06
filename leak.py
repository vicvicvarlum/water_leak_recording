import ftplib
import pyaudio
import wave
import math
import struct
import time
import os, errno
from ftplib import FTP

#User folder to be created/store the files, dont use blank spaces TODO: remove blank spaces
#Folder to be used at local and FTP
USER_FOLDER_NAME = 'victor_rel'
#seconds of tolerance to continue adding samples after the threshold has been reached
USER_MUTE_TOLERANCE = 5
#RMS Threshold to start recording
THRESHOLD = 0.05
#Minimun recording lenght (seconds), avoids false triggers
USER_REC_LENGHT = 2
#Py audio instance variables
FORM_1 = pyaudio.paInt16 # 16-bit resolution
CHANS = 1 # 1 channel
SAMP_RATE = 44100 # 44.1kHz sampling rate
CHUNK = 4096 # 2^12 samples for buffer
INPUT_BLOCK_TIME = 0.01
INPUT_FRAMES_PER_BLOCK = int(SAMP_RATE*INPUT_BLOCK_TIME)

#To obtain an RMS from 0 to 1, get the coefficient for 2^16/2 @16bit audio
NORMALIZE_16B = (1.0/32768.0)

#Operation variables

def get_rms(block):

    #Convert this string of bytes into a string of 16-bit samples
    #We will get one short out for each two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    sum_squares = 0.0
    for sample in shorts:
    # sample is a signed short in +/- 32768. 
    # normalize it to 1.0
        n = sample * NORMALIZE_16B
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

class Leak(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = THRESHOLD
        self.errorcount = 0

        #Calculations per user input (time base are x1 miliseconds)
        self.mute_tolerance = USER_MUTE_TOLERANCE * 100 #seconds 
        self.min_rec_lenth = USER_REC_LENGHT * 100
        #Operation and system variables 
        self.filename_audio = ""
        self.count = 0
        self.build_new_file_exists = False
        self.count_when_trigger = 0
        self.count_when_trigger_dots = 0
        self.append_samples = False 

        self.frames = []

        self.dots_mute_tolerance_counter = 0
        self.dots_total_seconds = int(self.mute_tolerance/100)

        self.ftp = FTP('ftp.lumenir-innovations.com')
        self.folders_ftp = []
        self.create_ftp_user_folder = False
        self.already_in_folder = False

        print ("Starting a new instance")


        #try:
        #    os.makedirs(USER_FOLDER_NAME)
        #except OSError as e:
        #    if e.errno != errno.EEXIST:
        #       raise
    
    def stop(self):
        self.stream.close()

    def open_mic_stream( self ):
        device_index = 1 #TODO: method to automate selection

        stream = self.pa.open(   format = FORM_1,
                                 channels = CHANS,
                                 rate = SAMP_RATE,
                                 input = True,
                                 input_device_index = 1,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    def listen(self):
        try:
            data = self.stream.read(INPUT_FRAMES_PER_BLOCK, exception_on_overflow = False)
        except IOError as e:
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )    

        if self.append_samples == False:
            self.count = 0

        #Convert from bytes to int and calculate RMS value of the samples
        rms_val = get_rms(data)

        if(rms_val > THRESHOLD):

            if  (self.build_new_file_exists == False):
                self.filename_audio = time.ctime().replace(" ","").replace(":","_") + "_sample.wav"
                print("File name started: ", self.filename_audio)
                self.build_new_file_exists = True

            print("T", self.count, rms_val)
            #Used for mute tolerance calculation
            self.count_when_trigger = self.count
            #Used for down counter
            self.count_when_trigger_dots = self.count
            #Proceed with storing the samples
            self.append_samples = True

                #Continue to append the samples to the list even when we havent met the threshold (on mute)
        if(self.append_samples == True and (self.count <= self.count_when_trigger + self.mute_tolerance )) :
            self.frames.append(data)
            if(self.count > self.count_when_trigger_dots+100 ):
                self.count_when_trigger_dots = self.count 
                self.dots_mute_tolerance_counter +=1
                print(self.dots_total_seconds-self.dots_mute_tolerance_counter, end=' ', flush=True)

        if(self.count > self.count_when_trigger + self.mute_tolerance and len(self.frames)!= 0):
            if self.count-self.mute_tolerance > self.min_rec_lenth:
                self.append_samples = False
                # save the audio frames as .wav file
                wavefile = wave.open(self.filename_audio,'wb')
                #wavefile = wave.open(USER_FOLDER_NAME+'/'+self.filename_audio,'wb')
                wavefile.setnchannels(CHANS)
                wavefile.setsampwidth(self.pa.get_sample_size(FORM_1))
                wavefile.setframerate(SAMP_RATE)
                wavefile.writeframes(b''.join(self.frames))
                wavefile.close()
                print("New file saved: ", self.filename_audio," total time (mS): ", self.count - self.mute_tolerance)

                """""
                try:
                    print (self.ftp.login(user='waterleak@lumenir-innovations.com', passwd = 'Lumen!r710!'))
                except ftplib.all_errors as e:
                    print ("Already logged in?: ", e)

                try:
                    self.ftp.dir(self.folders_ftp.append)

                    for line in self.folders_ftp:
                        print ("-", line)
                        if USER_FOLDER_NAME in line:
                            None
                            #print ("User folder exists, folder will not be created")
                            self.create_ftp_user_folder = False
                            break
                        else:
                            #print ('User folder doesnt exists, creating',USER_FOLDER_NAME,'folder')
                            self.create_ftp_user_folder = True
                    
                    if self.create_ftp_user_folder == True:
                        print ("To create new folder on ftp")
                        print (self.ftp.mkd(USER_FOLDER_NAME))
                        print ("My new created directoty is" , self.ftp.pwd())
                        self.create_ftp_user_folder = False
                        print (self.ftp.cwd(USER_FOLDER_NAME))
                        self.already_in_folder = True
                    else:
                        print ("No need for changing directory, my directory is: ", self.ftp.pwd())
                        None
                        #print (self.ftp.pwd())
                        #if self.ftp.pwd()==USER_FOLDER_NAME:
                        #    print("Already infolder")
                        #else:
                        #    print ("Working folder is", self.ftp.cwd(USER_FOLDER_NAME))

                    if self.already_in_folder == True:
                        None
                    else:
                        print (self.ftp.cwd(USER_FOLDER_NAME))
                        self.already_in_folder = True

                    print (self.ftp.storbinary('STOR '+self.filename_audio, open(self.filename_audio, 'rb')))
                    self.ftp.close()
                    return
 
                    
                except ftplib.all_errors as e:
                    print ("Error uploading: ", e)
                    self.ftp.close()
                    return

                self.frames.clear()
                self.build_new_file_exists = False
                self.count = 0
                self.dots_mute_tolerance_counter = 0
                """
            else:
                print("No file created, false trigger", self.count)
                self.frames.clear()
                self.build_new_file_exists = False
                self.count = 0
                self.dots_mute_tolerance_counter = 0
                self.append_samples = False

        self.count +=1

if __name__ == "__main__":
    lk = Leak()
    print("start")
    while(True):
        lk.listen()



