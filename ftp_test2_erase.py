from ftplib import FTP
import os, errno


import ftplib 

with ftplib.FTP('ftp.lumenir-innovations.com') as ftp:
    
    filename = 'SatOct2319_05_542021_sample.wav'
    
    try:    
        print(ftp.login('waterleak@lumenir-innovations.com', 'Lumen!r710!'))
        
        with open(filename, 'rb') as fp:
            
            res = print(ftp.storlines("STOR " + filename, fp))
            
            if not res.startswith('226 Transfer complete'):
                
                print('Upload failed')

    except ftplib.all_errors as e:
        print('FTP error:', e) 