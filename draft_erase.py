#pip install pipwin
#pipwin install pyaudio







errorcount = 0

USER_REC_LENGHT = REC_LENGHT * 100

RATE = 44100  
INPUT_BLOCK_TIME = 0.01
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)



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






rms_val = 0.0 #Placeholder to store rms converted val from chunk*sample_rate
count = 0 # loop iteration 

seconds_to_sample = 20 * 100 #in seconds first arg


filename_audio = ""


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


    count +=1
    #if(count >seconds_to_sample):
        
    

print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()
ftp.quit()



