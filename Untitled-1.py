

        self.ftp.dir(self.folders_ftp.append)

        for line in self.folders_ftp:
            print ("-", line)
            if USER_FOLDER_NAME in line:
                print ("User folder exists, folder will not be created")
                self.create_ftp_user_folder = False
            else:
                self.create_ftp_user_folder = True


        if self.create_ftp_user_folder:
            print ('User folder doesnt exists, creating',USER_FOLDER_NAME,'folder')
            print (self.ftp.mkd(USER_FOLDER_NAME))
            self.create_ftp_user_folder = False

        self.ftp.cwd('/'+USER_FOLDER_NAME+'/')


        
        print (self.ftp.login(user='waterleak@lumenir-innovations.com', passwd = 'Lumen!r710!'))
        print (self.ftp.login(user='waterleak@lumenir-innovations.com', passwd = 'Lumen!r710!'))
        self.ftp.dir(self.folders_ftp.append)