import pyaudio
p = pyaudio.PyAudio()
print("start")

with open("usb_devices.txt", 'a+') as myfile:
    for ii in range(p.get_device_count()):
        myfile.write(p.get_device_info_by_index(ii).get('name'))
        myfile.write("\n")

with open("usb_devices.txt", 'r') as myfile:
    count = 0
    for line  in myfile:
        if "USB" in line:
            print (count)
            break
        count+=1    