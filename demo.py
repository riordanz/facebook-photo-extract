from facebook_sekode import PhotoExtractor

#Define PhotoExtractor
PE = PhotoExtractor()
#Login
PE.login("email/username", "password")
#Getting Photo
PE.get_photos("username_target", limit_photo) #Limit Photo must be multiple of 12. as default = 12
#Export Photo
PE.export("folder")
