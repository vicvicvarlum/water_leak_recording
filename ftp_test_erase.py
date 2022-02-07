from ftplib import FTP
import os, errno

user_folder_name = "victor_rel"

ftp = FTP('ftp.lumenir-innovations.com')
folders_ftp = []

if ftp.sock is None:
    print("Socket is None.")
else:
    print("Socket is still assigned, but closed")

# check if open
try:
    ftp.voidcmd("NOOP")
except AttributeError as e:
    errorInfo = str(e).split(None, 1)[0]
    print(errorInfo)
    connected = False

print (ftp.voidcmd("NOOP"))

print (ftp.login(user='waterleak@lumenir-innovations.com', passwd = 'Lumen!r710!'))

print(ftp.dir(folders_ftp.append), "ok")

print(ftp.pwd())

for line in folders_ftp:
    print ("-", line)
    if 'Pablo' in line:
        print ("User folder exists, folder will not be created")
        create_ftp_user_folder = False
        break
    else:
        create_ftp_user_folder = True

print("var ftp create is: ", create_ftp_user_folder)

if (create_ftp_user_folder == True):
    create_ftp_user_folder = False
    print (ftp.mkd(user_folder_name))

ftp.cwd(user_folder_name) 
print(ftp.pwd())

print(os.listdir())
print("check")
print (ftp.voidcmd("NOOP"))
if ftp.sock is None:
    print("Socket is None.")
else:
    print("Socket is still assigned, but closed")


#localpath = os.path.join("victor_rel", name)

#print (ftp.storbinary('STOR '+ , open(, 'rb')))



