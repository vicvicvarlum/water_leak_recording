## 1. Upgrade to the latest libraries (optional)
* sudo apt-get update
* sudo apt-get upgrade

## 2. Install the pyaudio and portaudio libraries 
* sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
* sudo pip3 install pyaudio

## 3. Config userspace
* Open the file **spec_audio_dev.py** in edit mode 
* Modify the user folder to store the recordings under line 5 **user_folder_name = 'user'**
* Modify the user mute tolence (Seconds to continue recording after the RMS input is below threshold) under line 10 **user_mute_tolerance = 10**
* Adjust the threshold RMS value (Depends on the gain of the HiFiBerry hat) 
* Save the file

## 4. Use ThonnyIDE (optional)
* Navigate to the folder and Right click **spec_audio_dev.py** and select open **Thonny Python IDE**
* Modify the userspace params fasters and run the program

## 5. Run the script
* Navigate to the folder where the **spec_audio_dev.py** is located and open a terminal
* Execute **sudo python3 spec_audio_dev.py**
* Expect the device HiFiBerry to be listed on the console 
* Device is ready to start continously recording 